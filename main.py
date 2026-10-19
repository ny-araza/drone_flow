import sys
from pathlib import Path

from display import Display
from error import ParseError
from input import Input

if __name__ == "__main__":
    try:
        flag = sys.argv[1:]

        height = 960
        width = 1280

        if "--folder" in flag:
            if len(flag) != 2:
                raise ParseError(
                    "Flag --folder must be python " \
                    "main.py --folder <map_folder>"
                )
            path = Path(flag[1])
            if not path.is_dir():
                raise ParseError(
                    f"{flag[1]} is not a folder"
                )
            input: Input = Input(flag[1])
            input.choose_level()
            input.select_map_path()    
            display: Display = Display(input.map_path, width, height)
            display.display_window()
        else:
            if len(flag) != 1:
                raise ParseError(
                    "To run this program: " \
                    "python main.py <file_path>"
                )
            display: Display = Display(flag[0], width, height)
            display.display_window()

    except KeyboardInterrupt:
        print("\nPlease be patient!!")
    except Exception as e:
        print("An error occured: ", str(e))
