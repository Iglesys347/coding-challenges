import pytest
import redis
from redis.exceptions import ConnectionError

from codchal import db_utils as du
from codchal.settings import REDIS_HASH_KEY
from codchal.errors import RedisError

FAKE_USER = {"id": "1234",
             "xp": 10}


@pytest.fixture
def empty_redis():
    # using default settings
    client = redis.Redis(decode_responses=True)
    client.flushall()
    return client


@pytest.fixture
def redis_client():
    # using default settings
    client = redis.Redis(decode_responses=True)
    # populating Redis with one user informations
    client.hset(REDIS_HASH_KEY, FAKE_USER["id"], FAKE_USER["xp"])
    return client


def test_db_utils_check_db_running(empty_redis_client):
    assert du.check_db_running(empty_redis_client) == True


def test_db_utils_check_db_not_running():
    # defining a not running client
    client = redis.Redis("localhost", 6969)
    assert du.check_db_running(client) == False


def test_db_utils_add_user(empty_redis):
    assert du.add_user(empty_redis, FAKE_USER["id"]) == 1
    # testing that the user is well added
    assert empty_redis.hget(REDIS_HASH_KEY, FAKE_USER["id"]) == 0


def test_db_utils_add_user_exception_user_exists(redis_client):
    with pytest.raises(RedisError):
        du.add_user(redis_client, FAKE_USER["id"])


def test_db_utils_get_users(redis_client):
    assert du.get_users(redis_client) == [FAKE_USER["id"]]


def test_db_utils_get_users_empty(empty_redis):
    assert du.get_users(empty_redis) == []


def test_db_utils_get_user_xp_with_user_id(redis_client):
    assert du.get_user_xp(redis_client, FAKE_USER["id"]) == FAKE_USER["xp"]


def test_db_utils_get_user_xp_without_user_id(redis_client):
    assert du.get_user_xp(redis_client) == {FAKE_USER["id"]: FAKE_USER["xp"]}


def test_db_utils_get_user_xp_user_nexist_exception(empty_redis):
    with pytest.raises(RedisError):
        du.get_user_xp(empty_redis, FAKE_USER["id"])


def test_db_utils_del_user(redis_client):
    # check that the user exist before deletion
    assert int(redis_client.hget(
        REDIS_HASH_KEY, FAKE_USER["id"])) == FAKE_USER["xp"]
    assert du.del_user(redis_client, FAKE_USER["id"]) == True
    # check that the user does not exist anymore
    assert redis_client.hexists(REDIS_HASH_KEY, FAKE_USER["id"]) == False


def test_db_utils_del_user_user_nexist_exception(empty_redis):
    with pytest.raises(RedisError):
        du.del_user(empty_redis, FAKE_USER["id"])


def test_db_utils_add_xp(redis_client):
    amount = 10
    assert du.add_xp(redis_client, FAKE_USER["id"], amount) == True
    # checking the xp has been updated
    assert int(redis_client.hget(REDIS_HASH_KEY,
               FAKE_USER["id"])) == FAKE_USER["xp"] + amount


def test_db_utils_add_xp_user_nexists_exception(empty_redis):
    with pytest.raises(RedisError):
        du.add_xp(empty_redis, FAKE_USER["id"], 10)
