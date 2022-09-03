from bot import run_bot
from db_utils import check_db_running
from errors import DockerError, RedisError
from subprocess import DEVNULL, STDOUT, CalledProcessError, check_call

# checking that docker and redis are installed
try:
    check_call(["dpkg", "-s", "docker-ce"], stdout=DEVNULL, stderr=STDOUT)
except CalledProcessError:
    raise DockerError("Docker is not installed on this machine")
try:
    check_call(["dpkg", "-s", "redis"], stdout=DEVNULL, stderr=STDOUT)
except CalledProcessError:
    raise RedisError("Redis is not installed on this machine")

# checking that redis db is running
if not check_db_running():
    raise RedisError("Redis server is not running on the specified host/port")

# running the bot
run_bot()
