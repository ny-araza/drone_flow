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

    @staticmethod
    def get_drone_in_each_turn(
        current_zone: str,
        next_zone: str,
        drone: str,
        zone_drones: dict[str, list[str]]
    ) -> None:

        if current_zone != next_zone:
            if drone in zone_drones[current_zone]:
                zone_drones[current_zone].remove(drone)

            if drone not in zone_drones[next_zone]:
                zone_drones[next_zone].append(drone)
