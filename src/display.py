from .utils import read_file
from .parse import Parse

class Display:
    def __init__(self, map_path: str):
        parse: Parse = Parse()
        data = read_file(map_path)
        parse.parse(data)
