import sys
from .error import ParseError
from .input import Input
import os


if __name__ == "__main__":
    try:
        if not sys.argv[1:] or not \
                os.path.isdir(sys.argv[1:][0]):
            raise ParseError("'maps' folder does not exist")

        input: Input = Input(sys.argv[1:][0])
        input.choose_level()
        input.select_map_path()
        print(input.map_path)
    except KeyboardInterrupt:
        print("\nPlease be patient!!")
    except Exception as e:
        print(f"An error occured {e}")
