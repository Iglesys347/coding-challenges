# coding-challenges

Discord bot for coding challenges.

## Requirements

### Python dependancies

See [requirements.txt](requirements.txt)

### Other dependancies

- [docker](https://www.docker.com/)

## Setup

To setup the module, run:

```bash
python setup.py install
```

## Usage

### Specify the bot token

Specify the bot token in a file named `.token`.

### Run the bot

Run the bot with

```bash
python bot.py
```

## Settings

Settings can be tunned in [settings.py](settings.py):

### Bot settings

- `CHALLENGES_DIR` : dirrectory of the json challenges
- `DIFFICULTY_COLOR_MAP` : colors to display in discord according to difficulty levels
- `DIFFICULTY_XP_MAP` : amount of xp won according to difficulty levels
- `RANKS_FILE` : file containing the xp-rank mapping

### Redis DB settings

- `REDIS_HOST` : Redis host
- `REDIS_PORT` : Redis port
- `REDIS_DB` : Redis DB
- `REDIS_HASH_KEY` : Redis hash name

### Script handler settings

- `DEFAULT_DIR` : default dir for solutions scripts
- `FILE_EXT` : file extension-language mapping
- `KNOWN_LANG` : set of supported languages
- `DOCKER_IMG` : mapping language-docker image
