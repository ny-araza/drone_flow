class Utils:
    @staticmethod
    def read_file(file_path: str) -> str:
        data: str = ""
        with open(file_path, "r", encoding="utf-8") as fd:
            data = fd.read()
        return data

    @staticmethod
    def print_rgb(text: str, rgb: tuple[int, int, int]) -> None:
        r, g, b = rgb
        print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=" ")
