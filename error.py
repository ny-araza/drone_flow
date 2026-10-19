class ParseError(Exception):
    """Represent the parse error

        Attributes:
            message (str): The error message
    """
    def __init__(self, message: str = "") -> None:
        pass


class PathFindingError(Exception):
    """Represent the pathfinding error

        Attributes:
            message (str): The error message
    """
    def __init__(self, message: str = "") -> None:
        pass
