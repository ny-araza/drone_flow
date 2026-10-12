from typing import Any

from pydantic import ValidationError

from .connection import Connection
from .error import ParseError
from .validation import ZoneValidation
from .zone import Zone, ColorType, TypeZone


class Parse:
    def __init__(self) -> None:
        self.list_connections: list[Connection] = []
        self.list_zones: list[Zone] = []
        self.nb_drones: int = 0

    def check_unique_zone_name(
        self, name: str,
        zones_name: list[str]
    ) -> list[str]:
        if name in zones_name:
            return []
        zones_name.append(name)
        return zones_name

    def validate_zone(
        self, line: int, name: str, x: str, y: str, metadata_dict: dict[str, Any]
    ) -> bool:
        try:
            max_drones = metadata_dict.get("max_drones", None)
            if max_drones:
                n = int(max_drones)
                if n <= 0:
                    raise ParseError(
                        f"Line {line} "
                        "max_drones must be greater than 0"
                    )
            ZoneValidation(
                name=name,
                x=int(x),
                y=int(y),
                is_start=True,
                is_end=False,
                max_drones=metadata_dict.get("max_drones", 1),
                color=metadata_dict.get("color", "white"),
                type=metadata_dict.get("zone", "normal"),
            )
            return True
        except ValidationError as e:
            for error in e.errors():
                raise ParseError(
                    f"Line {line} "
                    f"{error['msg']}"
                )
            return False


    def sotck_zones(
        self,
        line: int,
        key: str,
        basedata: list[str],
        metadata_dict: dict[str, Any],
        exists_name: list[str],
        coords: list[tuple[int, int]],
        coords_set: set
    ) -> None:
        name, x, y = basedata
        coords.append((x, y))
        if (x, y) not in coords_set:
            coords_set.add((x, y))
        else:
            raise ParseError(
                f"Line {line} "
                f"The {(int(x), int(y))} {name} point is "
                "overlap with another zone point"
            )
        if self.check_unique_zone_name(name, exists_name):
            if self.validate_zone(line, name, x, y, metadata_dict):
                if key == "start_hub":
                    self.list_zones.append(
                        Zone(
                            name,
                            int(x),
                            int(y),
                            is_start=True,
                            is_end=False,
                            max_drones=metadata_dict.get("max_drones", 1),
                            color=metadata_dict.get("color", "black"),
                            type=metadata_dict.get("zone", "normal"),
                            image="./images/start_hub.png",
                        )
                    )
                elif key == "end_hub":
                    self.list_zones.append(
                        Zone(
                            name,
                            int(x),
                            int(y),
                            is_start=False,
                            is_end=True,
                            max_drones=metadata_dict.get("max_drones", 1),
                            color=metadata_dict.get("color", "black"),
                            type=metadata_dict.get("zone", "normal"),
                            image="./images/end_hub_50x50.png",
                        )
                    )
                elif key == "hub":
                    self.list_zones.append(
                        Zone(
                            name,
                            int(x),
                            int(y),
                            is_start=False,
                            is_end=False,
                            max_drones=metadata_dict.get("max_drones", 1),
                            color=metadata_dict.get("color", "black"),
                            type=metadata_dict.get("zone", "normal"),
                        )
                    )
                else:
                    raise ParseError(
                        f"Line {line} "
                        f"{key} key must be between <start_hub>, <hub>, <end_hub>"
                    )
        else:
            raise ParseError(
                f"Line: {line}"
                f"{name} is not an unique zone name"
            )

    def check_key_metadata(self,keys: list[str]) -> bool:
        all_key_metadata: list[str] = ["zone", "color", "max_drones"]
        for key in keys:
            if key not in all_key_metadata:
                return False
        return True

    def parse(self, data: str) -> None:
        if not ("start_hub" in data and "end_hub" in data):
            raise ParseError(
                f"Line: {line}"
                "map file must contain 'start_hub' and 'end_hub'"
                )
        temp: list[str] = data.split("\n")
        exists_name: list[str] = []
        coords: list[tuple[int, int]] = []
        coords_set = set()
        for tmp in temp:
            line = temp.index(tmp) + 1
            if not tmp.startswith("#") and tmp:
                item = tmp.split(":")
                if len(item) != 2:
                    raise ParseError(
                        f"Line {line} "
                        "One single ':' "
                        "per line must be present in the map file"
                    )
                key, value = item
                if key == "nb_drones":
                    try:
                        self.nb_drones = int(value)
                        if self.nb_drones <= 0:
                            raise ParseError(
                                f"Line {line} "
                                "'nb_drones' must be greater than 0 and int"
                            )
                        continue
                    except ValueError:
                        self.nb_drones = 0
                        raise ParseError(
                            f"Line {line} "
                            "'nb_drones' must be int and positive"
                        )
                basedata: list[str] = []
                if key != "connection":
                    cpt = 0
                    for c in value:
                        if c == "[" or c == "]":
                            cpt += 1
                    if cpt != 2:
                        raise ParseError(
                            f"Line {line} "
                            "The number of brackets must be two"
                            )
                    temp_value = value.split("[")
                    if not value.endswith("]"):
                        raise ParseError(
                            f"Line {line} "
                            "Metadata must be inside brackets [...]"
                        )
                    basedata = temp_value[0].strip(" ").split(" ")
                    if len(basedata) != 3:
                        raise ParseError(
                            f"Line {line} "
                            "An error occured on map file line: "
                            "line must be: <type_zone>: "
                            "<zone_name> <pos_x> <pos_y> "
                            "[<metadata_key>=<metadata_value>]"
                        )
                    zone_metadata = []
                    temp_temp_value = temp_value[1].split(" ")
                    for meta_val in temp_temp_value:
                        new_temp = meta_val.strip("[]")
                        if new_temp:
                            zone_metadata.append(str(new_temp))
                    metadata_dict: dict[str, Any] = {}
                    for temp_item in zone_metadata:
                        meta_key, meta_value = temp_item.split("=")
                        if len(temp_item.split("=")) != 2:
                            raise ParseError(
                                f"Line {line} "        
                                "Metadata must be [meta_data=value]"
                            )
                        metadata_dict.update({meta_key: meta_value})
                    if not self.check_key_metadata(list(metadata_dict.keys())):
                        raise ParseError(
                            f"Line {line} "
                            "metadata key must be "
                            "'zone', 'color' or 'max_drones'"
                        )
                    self.sotck_zones(line, key, basedata, metadata_dict, exists_name, coords, coords_set)
                elif key == "connection":
                    connect_data = value.split("[")
                    if len(connect_data) > 2:
                        raise ParseError(
                            f"Line {line} "   
                            "connection in mapfile must be <zone1>-<zone2> "
                            "[<metadata_key>=<metadata_value>]"
                        )
                    temp_base_con: str = ""
                    temp_meta_con: str = ""
                    if len(connect_data) == 1:
                        temp_base_con = connect_data[0]
                    elif len(connect_data) == 2:
                        temp_base_con = connect_data[0].strip(" []")
                        temp_meta_con = connect_data[1].strip(" []")
                    basedata_con = temp_base_con.split("-")
                    if len(basedata_con) != 2:
                        raise ParseError(
                            f"Line {line} "    
                            "connection in mapfile must be <zone1>-<zone2> "
                            "[<metadata_key>=<metadata_value>]"
                        )
                    metadata_con: list[str] = []
                    temp_metadata: dict[str, Any] = {}
                    if temp_meta_con:
                        metadata_con = temp_meta_con.split("=")
                        if len(metadata_con) != 2:
                            raise ParseError(
                                f"Line {line} "    
                                "connection in mapfile "
                                "must be <zone1>-<zone2> "
                                "[<metadata_key>=<metadata_value>]"
                            )
                        key, value = metadata_con
                        if key != "max_link_capacity" or int(value) <= 0:
                            raise ParseError(
                                f"Line {line} "
                                "For connection metadakey must be "
                                "[max_link_capacity: <metadata_value>] "
                                "(NB: metadata_value > 0)"
                            )
                        try:
                            temp_metadata.update({key: int(value)})
                        except ValueError:
                            raise ParseError(
                                f"Line {line} "
                                "In connection: metadata_value "
                                "must be > 0 and numbers"
                            )
                    zone1: Zone = Zone(
                        name="",
                        color=ColorType.CRIMSON,
                        is_end=False,
                        is_start=False,
                        max_drones=1,
                        type=TypeZone.NORMAL,
                        x=0,
                        y=0,
                    )
                    zone2: Zone = Zone(
                        name="",
                        color=ColorType.CRIMSON,
                        is_end=False,
                        is_start=False,
                        max_drones=1,
                        type=TypeZone.NORMAL,
                        x=0,
                        y=0,
                    )
                    z1, z2 = basedata_con
                    for zone in self.list_zones:
                        if zone.name == z1.strip(" "):
                            zone1 = zone
                            break

                    if not zone1.name:
                        raise ParseError(
                            f"Line {line} "
                            f"The {z1} is not in zone list"
                            )

                    for zone in self.list_zones:
                        if zone.name == z2.strip(" "):
                            zone2 = zone
                            break

                    if not zone2.name:
                        raise ParseError(
                            f"Line {line} "
                            f"The {z2} is not in zone list"
                            )

                    connection: Connection = Connection(
                        zone1, zone2, temp_metadata
                    )

                    self.list_connections.append(connection)
