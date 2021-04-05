# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class BadLineArguments(Error):
    """Raised when the input value is too large"""
    pass


class InvalidPointsRange(Error):
    """Raised when the input value is too large"""
    pass


class InvalidNumberArguments(Error):
    """Raised when the input value is too large"""
    pass


class InvalidArgumentType(Error):
    """Raised when the input value is too large"""
    pass