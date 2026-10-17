class ParseError(Exception):
    """Represent the parse error

        Attributes:
            message (str): The error message
    """
    def __init__(self, message: str = "") -> None:
        print(f"Parsing error: {message}")


class PathFindingError(Exception):
    """Represent the pathfinding error
    
        Attributes:
            message (str): The error message
    """
    def __init__(self, message: str = "") -> None:
        print(f"PahtFinding error: {message}")
