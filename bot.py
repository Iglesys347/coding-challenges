"""Discord bot command description."""

import json
import os
from random import choice
import discord
from discord.ext import commands
import redis

from challenge import Challenge
from errors import RedisError
from db_utils import add_user, add_xp, get_user_xp
from handler import SolHandler
from checker import check_script

from settings import (CHALLENGES_DIR, DIFFICULTY_COLOR_MAP,
                      DIFFICULTY_XP_MAP, REDIS_DB, REDIS_HOST, REDIS_PORT, RANKS_FILE)

intents = discord.Intents.default()
intents.message_content = True


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                           db=REDIS_DB, decode_responses=True)


bot = commands.Bot(commands.when_mentioned_or("!"), intents=intents,
                   description="Coding challenges Discord bot.")


@bot.command(help="Select and start a random challenge")
async def challenge(ctx):
    """Select a random challenge and wait for the user solution."""
    def random_challenge():
        """Select random challenge from json challenges files in `CHALLENGES_DIR`."""
        chal_id = choice(os.listdir(CHALLENGES_DIR)).split(".")[0]
        return Challenge(chal_id, CHALLENGES_DIR)

    def check(mess):
        """Check that a message is well formed for solution.
        
        The message must match the 4 conditions to be considered as a solution:
            - message is not written by the bot itself
            - message starts with '```'
            - message written in the same challenge as the command !challenge
            - message written by the same user than the one who used the command !challenge
        """
        return mess.author != bot.user and mess.content.startswith("```") \
            and mess.channel == ctx.channel and mess.author == ctx.author

    chal = random_challenge()

    embed = discord.Embed(title=chal.name, description=chal.desc,
                          color=DIFFICULTY_COLOR_MAP[chal.difficulty])
    embed.add_field(name="Input", value="\n".join(elt[0] for elt in chal.examples),
                    inline=True)
    embed.add_field(name="Output", value="\n".join(elt[1] for elt in chal.examples),
                    inline=True)
    await ctx.send(embed=embed)

    solution = await bot.wait_for('message', check=check)
    # adding an emoji to the message so the user know its solution is taken into account
    await solution.add_reaction("👨‍🦼")
    solution = SolHandler(solution.content)

    score = check_script(solution.script_filename, chal)

    await ctx.send(f"Your score is {score}/{chal.max_score}")

    try:
        add_user(redis_client, ctx.message.author.id)
    except RedisError:
        pass

    # winning XP
    if score == chal.max_score:
        xp_won = DIFFICULTY_XP_MAP[chal.difficulty]
        add_xp(redis_client, ctx.message.author.id, xp_won)
        await ctx.send(f"Well done! You won {xp_won} XP!")
    else:
        await ctx.send("Your code does not pass all the test, no XP won!")

    # await ctx.send(elt)


@bot.command(help="Display the user's amount of XP")
async def xp(ctx):
    """Display the use's amount of XP."""
    user_id = ctx.message.author.id
    try:
        xp_amount = get_user_xp(redis_client, user_id)
        await ctx.send(f"You currently have {xp_amount} points of experience.")
    except RedisError:
        await ctx.send("You haven't completed any challenge! You have 0 points of experience.")


@bot.command(help="Display the user's rank")
async def rank(ctx):
    """Display the user's rank."""
    user_id = ctx.message.author.id
    try:
        xp_amount = get_user_xp(redis_client, user_id)
        rank_name = xp_to_rank(xp_amount)
        if rank is not None:
            await ctx.send(f"Your are currently a {rank_name}.")
        else:
            await ctx.send("Sorry, your rank is unknown.")
    except RedisError:
        await ctx.send("You haven't completed any challenge! You don't have a rank.")


def xp_to_rank(xp_amount):
    """Convert an amount of XP into a rank using `RANKS_FILE` correspondance."""
    with open(RANKS_FILE, "r", encoding="utf8") as file:
        ranks = json.load(file)
    for rank_name in ranks:
        if rank_name["lower_bound"] < xp_amount < rank_name["upper_bound"]:
            return rank_name["rank"]
    return None


def run_bot():
    """Run the bot."""
    # read bot token
    with open(".token", "r", encoding="utf8") as file:
        token = file.read()
    bot.run(token)
