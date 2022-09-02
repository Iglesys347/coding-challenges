import redis

from errors import RedisError
from settings import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_HASH_KEY


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                           db=REDIS_DB, decode_responses=True)


# Defining some usefull decorators
def check_user_exists(func):
    def inner(client, user_id, *args, **kargs):
        if not client.hexists(REDIS_HASH_KEY, user_id) and user_id is not None:
            raise RedisError(f"User with ID {user_id} does not exists.")
        return func(client, user_id, *args, **kargs)
    return inner


def check_user_nexists(func):
    def inner(client, user_id, *args, **kargs):
        if client.hexists(REDIS_HASH_KEY, user_id):
            raise RedisError(f"User with ID {user_id} does not exists.")
        return func(client, user_id, *args, **kargs)
    return inner


@check_user_nexists
def add_user(client, user_id):
    return client.hset(REDIS_HASH_KEY, user_id, 0)


def get_users(client):
    return client.hkeys(REDIS_HASH_KEY)


@check_user_exists
def get_user_xp(client, user_id=None):
    if user_id is None:
        return client.hgetall(REDIS_HASH_KEY)
    return int(client.hget(REDIS_HASH_KEY, user_id))


@check_user_exists
def del_user(client, user_id):
    return bool(client.hdel(REDIS_HASH_KEY, user_id))


@check_user_exists
def add_xp(client, user_id, xp):
    return bool(client.hincrby(REDIS_HASH_KEY, user_id, xp))


@check_user_exists
def remove_xp(client, user_id, xp):
    return bool(client.hincrby(REDIS_HASH_KEY, user_id, -xp))


@check_user_exists
def reset_xp(client, user_id=None):
    """Set the xp to 0 of specified user or all users by default."""
    if user_id is None:
        for user in get_users():
            reset_xp(user)
    return client.hset(REDIS_HASH_KEY, user_id, 0)


def flush(client):
    """Drop the database."""
    return client.flushall()


if __name__ == "__main__":
    x = get_user_xp(redis_client, "non")
    print(x)
