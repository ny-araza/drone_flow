import os
from .error import ParseError
from colorama import Fore, Style


class Input:
    def __init__(
            self,
            map_folder: str = "maps",
            sub_folder_map: list[str] = []
            ):
        self.map_folder = map_folder
        self.sub_folder = sub_folder_map
        self.map_choosen = ""

    def display_map_choice(self) -> None:
        if not os.path.isdir(self.map_folder):
            raise ParseError("'maps' must be a dir")

        print("")
        print(Fore.RED + "---FLY-IN---" + Style.RESET_ALL)
        print("\nAll the map:\n")
        for i in range(len(self.sub_folder)):
            print(i, end=" ")
            print(Fore.GREEN + self.sub_folder[i] + Style.RESET_ALL)

    def choose_map(self) -> str:
        map_choosen: str = ""

        def check_user_choice(user_choice: str) -> int:
            try:
                choice = int(user_choice)
                if choice >= 0 and choice < 5:
                    return choice
                return -1
            except ValueError:
                return -1

        while not map_choosen:
            choice = check_user_choice(
                input("\nChoose 0-4 between these maps = ")
            )
            if choice == -1:
                continue
            for i in range(len(self.sub_folder)):
                if i == choice:
                    self.map_choosen = self.sub_folder[i]
                    return "One map choosen"
        return ""
