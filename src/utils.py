from .zone import Zone

class Utils:
    @staticmethod
    def read_file(file_path: str) -> str:
        data: str = ""
        with open(file_path, "r", encoding="utf-8") as fd:
            data = fd.read()
        return data

    @staticmethod
    def display_zone(zones: list[Zone]) -> None:
        for index, zone in enumerate(zones):
            print(f"\n {index}")
            print(f"name: {zone.name}")
            print(f"type: {zone.type}")
            print(f"color: {zone.color}")
            print(f"is_start: {zone.is_start}")
            print(f"is_end: {zone.is_end}")
            print(f"max_drones: {zone.max_drones}")
