"""Main script of Coding-Challenges.

This scripts does the following 3 things:
    - check that redis & docker are installed
    - check that a redis server is running on the specified host/port
    - run the discord bot
"""

from subprocess import DEVNULL, STDOUT, CalledProcessError, check_call
import redis

from bot import run_bot
from db_utils import check_db_running
from errors import DockerError, RedisError

from settings import REDIS_HOST, REDIS_PORT, REDIS_DB

# checking that docker and redis are installed
try:
    check_call(["dpkg", "-s", "docker-ce"], stdout=DEVNULL, stderr=STDOUT)
except CalledProcessError as exc:
    raise DockerError("Docker is not installed on this machine") from exc
try:
    check_call(["dpkg", "-s", "redis"], stdout=DEVNULL, stderr=STDOUT)
except CalledProcessError as exc:
    raise RedisError("Redis is not installed on this machine") from exc

client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                     db=REDIS_DB, decode_responses=True)

# checking that redis db is running
if not check_db_running(client):
    raise RedisError("Redis server is not running on the specified host/port")

# running the bot
run_bot()
