"""Project settings."""

# dirrectory of the json challenges
CHALLENGES_DIR = "./challenges/"
# colors to display in discord according to difficulty levels
DIFFICULTY_COLOR_MAP = {"easy": 0x00FF00,
                        "medium": 0xFF9900,
                        "hard": 0xFF0000}
# amount of xp won according to difficulty levels
DIFFICULTY_XP_MAP = {"easy": 1,
                     "medium": 2,
                     "hard": 3}

# file containing the xp-rank mapping
RANKS_FILE = "ranks.json"

# Redis DB settings
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HASH_KEY = "users"

# default dir for solutions scripts
DEFAULT_DIR = "./scripts/"
# file extension-language mapping
FILE_EXT = {"py": "python"}
# set of supported languages
KNOWN_LANG = {"python"}

# mapping language-docker image
DOCKER_IMG = {"python": "python:3"}
