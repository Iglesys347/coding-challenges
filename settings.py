"""Project settings."""

CHALLENGES_DIR = "./challenges/"
DIFFICULTY_COLOR_MAP = {"easy": 0x00FF00,
                        "medium": 0xFF9900,
                        "hard": 0xFF0000}
DIFFICULTY_XP_MAP = {"easy": 1,
                     "medium": 2,
                     "hard": 3}

RANKS_FILE = "ranks.json"

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HASH_KEY = "users"


DEFAULT_DIR = "./scripts/"
FILE_EXT = {"py": "python"}
KNOWN_LANG = {"python"}

DOCKER_IMG = {"python": "python:3"}
