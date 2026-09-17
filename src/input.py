import os
from .error import ParseError
from colorama import Fore, Style


class Input:
    def __init__(
            self,
            map_folder: str = "maps",
            ):
        self.map_folder: str = map_folder
        self.sub_folder: list[str] = self.get_subfolders(map_folder)
        self.map_choosen: str = ""
        self.map_path: str = ""

    @staticmethod
    def display_map_choice(
            sub_folder: list[str]
            ) -> None:
        for i in range(len(sub_folder)):
            print(i, end=" ")
            print(Fore.GREEN + sub_folder[i] + Style.RESET_ALL)

    @staticmethod
    def get_subfolders(path: str) -> list[str]:
        sub_folder = []
        with os.scandir(path) as d:
            for e in d:
                sub_folder.append(e.name)
        return sub_folder

    @staticmethod
    def check_user_choice(
            user_choice: str,
            sub_folder: list[str]
            ) -> int:
        try:
            choice = int(user_choice)
            if choice >= 0 and choice < len(sub_folder):
                return choice
            return -1
        except ValueError:
            return -1

    def choose_level(self) -> None:
        print("")
        print(Fore.RED + "---FLY-IN---" + Style.RESET_ALL)
        print("\nAll the map:\n")
        if not os.path.isdir(self.map_folder):
            raise ParseError("'maps' must be a dir")
        self.display_map_choice(self.sub_folder)

        while not self.map_choosen:
            choice = self.check_user_choice(
                input(
                    f"\nChoose 0-{len(self.sub_folder) - 1} "
                    "between these maps = "
                    ),
                self.sub_folder
            )
            if choice == -1:
                continue
            for i in range(len(self.sub_folder)):
                if i == choice:
                    self.map_choosen = os.path.join(
                        self.map_folder,
                        self.sub_folder[i]
                    )
                    break

    def select_map_path(self) -> None:
        print(
            "\nThis is all the available "
            f"map for ({self.map_choosen})\n"
        )
        all_map_path: list[str] = self.get_subfolders(self.map_choosen)
        Input.display_map_choice(all_map_path)

        while not self.map_path:
            choice = self.check_user_choice(
                input(
                    f"\nChoose 0-{len(all_map_path) - 1} "
                    "between these maps = "
                    ),
                all_map_path
            )
            if choice == -1:
                continue
            for i in range(len(all_map_path)):
                if i == choice:
                    self.map_path = os.path.join(
                        self.map_choosen,
                        all_map_path[i]
                    )
                    break
