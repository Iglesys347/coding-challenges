"""Module containing utils function to manipulate the DB."""

from redis.exceptions import ConnectionError

from codchal.errors import RedisError
from codchal.settings import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_HASH_KEY


def check_db_running(client):
    """Check that the Redis DB is running.

    Parameters
    ----------
    client : redis.Redis
        The Redis client.

    Returns
    -------
    bool
        True if the Redis DB is running on the expected host/port, False otherwise.
    """
    try:
        ping_res = client.ping()
        return ping_res
    except ConnectionError:
        return False


# Defining some usefull decorators
def check_user_exists(func):
    """Decorator function to check if user exists in DB."""
    def inner(client, user_id, *args, **kargs):
        if not client.hexists(REDIS_HASH_KEY, user_id) and user_id is not None:
            raise RedisError(f"User with ID {user_id} does not exists.")
        return func(client, user_id, *args, **kargs)
    return inner


def check_user_nexists(func):
    """Decorator function to check if does not exists in DB."""
    def inner(client, user_id, *args, **kargs):
        if client.hexists(REDIS_HASH_KEY, user_id):
            raise RedisError(f"User with ID {user_id} does not exists.")
        return func(client, user_id, *args, **kargs)
    return inner


@check_user_nexists
def add_user(client, user_id):
    """Add user to the DB.

    Parameters
    ----------
    client : redis.Redis
        The Redis client.
    user_id : str
        The new user ID.

    Returns
    -------
    int
        The result of HSET command. 1 if no problem encountered, 0 otherwise.
    """
    return client.hset(REDIS_HASH_KEY, user_id, 0)


def get_users(client):
    """Return the users IDs saved in DB.

    Parameters
    ----------
    client : redis.Redis
        The Redis client.

    Returns
    -------
    list
        The list of users ID saved in the DB.
    """
    return client.hkeys(REDIS_HASH_KEY)


def get_user_xp(client, user_id=None):
    """Return the XP amount of an user or if user not specified of all users.

    Parameters
    ----------
    client : redis.Redis
        The Redis client.
    user_id : str, default=None
        The user ID.

    Returns
    -------
    int | dict
        The amount of XP of the given user is user is not None, otherwise returns the dict of all
        users XP (the key is the user ID and the value its XP amount).
    """
    if user_id is None:
        return client.hgetall(REDIS_HASH_KEY)
    if not client.hexists(REDIS_HASH_KEY, user_id) and user_id is not None:
        raise RedisError(f"User with ID {user_id} does not exists.")
    return int(client.hget(REDIS_HASH_KEY, user_id))


@check_user_exists
def del_user(client, user_id):
    """Delete an user from DB.

    Parameters
    ----------
    client : redis.Redis
        The Redis client.
    user_id : str
        The user ID.

    Returns
    -------
    bool
        True if the user has been successfully deleted, false otherwise.
    """
    return bool(client.hdel(REDIS_HASH_KEY, user_id))


@check_user_exists
def add_xp(client, user_id, xp):
    """Add the given amount of XP to an user.

    Parameters
    ----------
    client : redis.Redis
        The Redis client.
    user_id : str
        The user ID.
    xp : int
        The amount of XP to add to the user.

    Returns
    -------
    bool
        True if the operation were successfull, False otherwise.
    """
    return bool(client.hincrby(REDIS_HASH_KEY, user_id, xp))


@check_user_exists
def remove_xp(client, user_id, xp):
    """Remove the given amount of XP to an user.

    Parameters
    ----------
    client : redis.Redis
        The Redis client.
    user_id : str
        The user ID.
    xp : int
        The amount of XP to remove from the user.

    Returns
    -------
    bool
        True if the operation were successfull, False otherwise.
    """
    return bool(client.hincrby(REDIS_HASH_KEY, user_id, -xp))


def reset_xp(client, user_id=None):
    """Set the xp to 0 of the specified user or for all users by default.

    Parameters
    ----------
    client : redis.Client
        The Redis client.
    user_id : str, default=None
        The user ID.
    """
    if user_id is None:
        for user in get_users(client):
            reset_xp(client, user_id=user)
    return bool(client.hset(REDIS_HASH_KEY, user_id, 0))


def flush(client):
    """Flush the database.

    Parameters
    ----------
    client : redis.Redis
        The Redis client.

    Returns
    -------
    bool
        True if the operation were successfull, False otherwise.
    """
    return client.flushall()
