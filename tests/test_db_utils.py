import pytest
import redis
from redis.exceptions import ConnectionError

from codchal import db_utils as du

@pytest.mark.parametrize
def redis_client():
    # using default settings
    client = redis.Redis()
    return client

def test_db_utils_check_db_running(redis_client):
    assert du.check_db_running(redis_client) == True

def test_db_utils_check_db_not_running():
    # defining a not running client
    client = redis.Redis("localhost", 6969)
    with pytest.raises(ConnectionError):
        du.check_db_running(client)

