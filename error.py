"""Represent error class."""


class ParseError(Exception):
    """Represent the parse error.

    Attributes:
        message (str): The error message
    """

    def __init__(self, message: str = "") -> None:
        """Represent the constructor fo the ParseError class.

        Args:
            messages (str): The message error
        """
        super().__init__(message)


class PathFindingError(Exception):
    """Represent the pathfinding error.

    Attributes:
        message (str): The error message
    """

    def __init__(self, message: str = "") -> None:
        """Represent the constructor of the pathfindingError.

        Args:
            message (str): The message error
        """
        super().__init__(message)
