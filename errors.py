class SolutionFormatError(Exception):
    """Raised when the solution's format is not valid."""


class LanguageError(Exception):
    """Raised when the language is not valid."""


class RedisError(Exception):
    """Raised when error occur in Redis DB."""


class UserError(Exception):
    """Rasied when error occur in User class."""
