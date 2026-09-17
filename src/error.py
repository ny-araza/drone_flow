class ParseError(Exception):
    def __init__(self, message: str = "") -> None:
        print(f"Parsing error: {message}")
