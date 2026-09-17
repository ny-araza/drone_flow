import sys
from .error import ParseError
from .input import Input

if __name__ == "__main__":
    try:
        if not sys.argv[1:]:
            raise ParseError("'maps' folder does not exist")
        sub_folder = [
            "challenger",
            "easy",
            "hard",
            "medium",
            "perso"
        ]
        input: Input = Input(sys.argv[1:][0], sub_folder)
        input.choose_map()
        print(input.map_choosen)
    except KeyboardInterrupt:
        print("\nPlease be patient!!")
    except Exception as e:
        print(f"An error occured {e}")
