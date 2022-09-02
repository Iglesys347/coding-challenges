import json
import os
from random import choice
import discord
from discord.ext import commands
from challenge import Challenge
from errors import RedisError
from db_utils import add_user, add_xp, get_user_xp
from handler import SolHandler
from checker import check_script
import redis

from settings import CHALLENGES_DIR, DIFFICULTY_COLOR_MAP, DIFFICULTY_XP_MAP, REDIS_DB, REDIS_HOST, REDIS_PORT, RANKS_FILE

intents = discord.Intents.default()
intents.message_content = True


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                           db=REDIS_DB, decode_responses=True)


bot = commands.Bot(commands.when_mentioned_or("!"), intents=intents,
                   description="Coding challenges Discord bot.")

# TODO function that chekcs on bot load that redis is running.


@bot.command(help="Select and start a random challenge.")
async def challenge(ctx):
    def random_challenge():
        chal_id = choice(os.listdir(CHALLENGES_DIR)).split(".")[0]
        return Challenge(chal_id, CHALLENGES_DIR)

    def check(m):
        return m.author != bot.user and m.content.startswith("```") and m.channel == ctx.channel and m.author == ctx.author

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


@bot.command(help="Display the user's amount of XP.")
async def xp(ctx):
    user_id = ctx.message.author.id
    try:
        xp = get_user_xp(redis_client, user_id)
        await ctx.send(f"You currently have {xp} points of experience.")
    except RedisError:
        await ctx.send("You haven't completed any challenge! You have 0 points of experience.")


@bot.command(help="Display the user's rank.")
async def rank(ctx):
    user_id = ctx.message.author.id
    try:
        xp = get_user_xp(redis_client, user_id)
        rank = xp_to_rank(xp)
        if rank is not None:
            await ctx.send(f"Your are currently a {rank}.")
        else:
            await ctx.send("Sorry, your rank is unknown.")
    except RedisError:
        await ctx.send("You haven't completed any challenge! You don't have a rank.")


def xp_to_rank(xp):
    with open(RANKS_FILE) as file:
        ranks = json.load(file)
    for rank in ranks:
        if rank["lower_bound"] < xp < rank["upper_bound"]:
            return rank["rank"]


bot.run("MTAwOTA1NzgxODY4NDQyODMwOA.G1wAsz.XRVOqc5PvVXwEncyHySFXM4X-bmB60EWg-kgqE")
