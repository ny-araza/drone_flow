from .utils import read_file
from .parse import parse

class Display:
    def __init__(self, map_path: str):
        self.data = read_file(map_path)
        parse(self.data)
