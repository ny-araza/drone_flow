import sys
from .error import ParseError
from .input import Input
import os


def get_subfolders(path: str) -> list[str]:
    sub_folder = []
    with os.scandir(path) as d:
        for e in d:
            if os.path.isdir(e):
                sub_folder.append(e.name)
    return sub_folder


if __name__ == "__main__":
    try:
        if not sys.argv[1:]:
            raise ParseError("'maps' folder does not exist")

        sub_folder: list[str] = get_subfolders(sys.argv[1:][0])
        input: Input = Input(sys.argv[1:][0], sub_folder)
        input.choose_map()
        print(input.map_choosen)
    except KeyboardInterrupt:
        print("\nPlease be patient!!")
    except Exception as e:
        print(f"An error occured {e}")
