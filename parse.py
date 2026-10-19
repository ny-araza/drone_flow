from typing import Any

from pydantic import ValidationError

from connection import Connection
from error import ParseError
from validation import ZoneValidation
from zone import ColorType, TypeZone, Zone
from color import color_rgb

class Parse:
    """Represent the parse of the map file.txt

        Public Methods:
            parse: Parse the map file and 
            raise an error if map is not valid
    """
    def __init__(self) -> None:
        """Constructor of the Parse class
        """
        self.list_connections: list[Connection] = []
        self.list_zones: list[Zone] = []
        self.nb_drones: int = 0

    def _check_unique_zone_name(
                self, name: str,
                zones_name: list[str]
            ) -> list[str]:
        """Check if all zone define in mapefile is unique

            Args:
                name (str): current zone name
                zones_name (list[str]): all zone already define before
            
            Returns:
                the new zone list
        """
        if name in zones_name:
            return []
        zones_name.append(name)
        return zones_name

    def _validate_zone(
        self,
        line: int,
        name: str,
        x: str,
        y: str,
        metadata_dict: dict[str, Any],
        map_path: str
    ) -> bool:
        """Check if the zone define is valid using pydantic

            Args:
                line (int): the number of line (for error debuging)
                name (str): The zone name to validate
                x (str): the x position of the zone in map
                y (str): the y position of the zone in map
                metadata_dict (dict[str, Any]): All the metadata zone
                map_path (str): path of the mapfile (for error debuging)
        
            Returns:
                valid or not valid
        """
        try:
            max_drones = metadata_dict.get("max_drones", None)
            if max_drones:
                n = int(max_drones)
                if n <= 0:
                    raise ParseError(
                        f"Line {line} max_drones "
                        "must be greater than 0"
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
                raise ParseError(f"{map_path}: Line {line} {error['msg']}")
            return False

    def _sotck_zones(
        self,
        line: int,
        key: str,
        basedata: list[str],
        metadata_dict: dict[str, Any],
        exists_name: list[str],
        coords: list[tuple[str, str]],
        coords_set: set[tuple[str, str]],
        map_path: str,
        width: int,
        height: int
    ) -> None:
        """Stock the zone found into a list of zone

            Args:
                key (str): key that check if value is zone or connexion
                basedata (list[str]): name, posx, posy (zone data)
                metadata_dict (dict[str, Any]): the metadata for the current zone
                exists_name (list[str]): all the zone name already defined before
                coords (list[tuple[str, str]]): all the coord already defined before
                coords_set (set[tuple[str, str]]): Use to check is other coords 
                is overlapping another coords
                map_path (str): the path of the map
                line (int): the cuurent line
                width (int): the width of the window
                height (int): the height of the window
        """
        name, x, y = basedata

        if not (
                int(x) < width and int(x) > -(width / 2)
            ) or not (
                    int(y) < height and int(y) > -(height / 2)
                ):
            raise ParseError(
                f"{map_path}: "
                f"Line {line} "
                f"Coords must be between {(width, height)}"
            )

        coords.append((x, y))
        if (x, y) not in coords_set:
            coords_set.add((x, y))
        else:
            raise ParseError(
                f"{map_path}: "
                f"Line {line} "
                f"The {(int(x), int(y))} {name} point is "
                "overlap with another zone point"
            )
        if self._check_unique_zone_name(name, exists_name):
            if self._validate_zone(line, name, x, y, metadata_dict, map_path):
                if key == "start_hub":
                    color = metadata_dict.get("color", "black")
                    if color not in color_rgb.keys():
                        color = "black"
                    self.list_zones.append(
                        Zone(
                            name,
                            int(x),
                            int(y),
                            is_start=True,
                            is_end=False,
                            max_drones=metadata_dict.get("max_drones", 1),
                            color=color,
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
                        f"{map_path}: "
                        f"Line {line} "
                        f"{key} key must be between <start_hub>, "
                        "<hub>, <end_hub>"
                    )
        else:
            raise ParseError(
                f"{map_path}: Line: {line}{name} is not an unique zone name"
            )

    def _check_key_metadata(self, keys: list[str]) -> bool:
        """Check if all key in metadata is valid

            Args:
                keys (list[str]): list of keys in a metadata for current zone
            
            Returns:
                bool
        """
        all_key_metadata: list[str] = ["zone", "color", "max_drones"]
        for key in keys:
            if key not in all_key_metadata:
                return False
        return True

    def parse(self, data: str, map_path: str, width: int, height: int) -> None:
        """Main parse, get the map path, stock all 
            zone valid and connexion valid in a list

            Args:
                data (str): The mapfile file read
                map_path (str): the path of the map
                width (int): width of the pygame window
                height (int): height of the pygame window
        """
        if not ("start_hub" in data and "end_hub" in data):
            raise ParseError(
                f"{map_path}: map file must contain 'start_hub' and 'end_hub'"
            )

        temp: list[str] = data.split("\n")
        exists_name: list[str] = []
        coords: list[tuple[str, str]] = []
        coords_set: set[tuple[str, str]] = set()
        is_nb_drones: bool = False

        for tmp in temp:
            line = temp.index(tmp) + 1
            if not tmp.startswith("#") and tmp:
                hash_temp = tmp.split("#")
                item = tmp.split(":")
                item = hash_temp[0].strip().split(":")
                print(item)
                if len(item) != 2:
                    raise ParseError(
                        f"{map_path}: "
                        f"Line {line} "
                        "One single ':' "
                        "per line must be present in the map file"
                    )
                key, value = item
                if not is_nb_drones and key == "nb_drones":
                    try:
                        self.nb_drones = int(value)
                        is_nb_drones = True
                        if self.nb_drones <= 0 or self.nb_drones > 100:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} "
                                "'nb_drones' must be greater than 0 and "
                                "less than or equal to 100"
                            )
                        continue
                    except ValueError:
                        raise ParseError(
                            f"{map_path}: "
                            f"Line {line}, 'nb_drones' must be int and positive"
                        )
                basedata: list[str] = []
                if is_nb_drones and key == "nb_drones":
                    raise ParseError(
                        f"{map_path} "
                        f"Line {line} "
                        "Only one nb_drones must declared in map file"
                    )
                if key != "connection":
                    if self.nb_drones <= 0:
                        raise ParseError(
                            "<nb_drones> must be the "
                            "top of the map file"
                        )

                    brackets_test = value.split("[")

                    if len(brackets_test) > 1:
                        cpt = 0
                        for c in value:
                            if c == "[" or c == "]":
                                cpt += 1
                        if cpt != 2:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} The number of "
                                "brackets must be two"
                            )

                    temp_value = value.split("[")
                    hash_comment = value.split("#")
                    temp_value = hash_comment[0].split("[")

                    if len(brackets_test) > 1:
                        if len(temp_value[0].split(" ")) != 5:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} Each line must "
                                "be separated by one space"
                            )
                        if not hash_comment[0].strip().endswith("]"):
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} Metadata must "
                                "be inside brackets [...]"
                            )

                    basedata = temp_value[0].strip(" ").split(" ")

                    if len(basedata) != 3:
                        raise ParseError(
                            f"{map_path}: "
                            f"Line {line} "
                            "An error occured on map file line: "
                            "line must be: <type_zone>: "
                            "<zone_name> <pos_x> <pos_y> "
                            "[<metadata_key>=<metadata_value>]"
                        )

                    zone_metadata = []
                    temp_temp_value = []

                    if len(brackets_test) > 1:
                        temp_temp_value = temp_value[1].split(" ")

                    metadata_dict: dict[str, Any] = {}

                    if not temp_temp_value:
                        metadata_dict = {}
                    for meta_val in temp_temp_value:
                        new_temp = meta_val.strip("[]")
                        if new_temp:
                            zone_metadata.append(str(new_temp))
                    for temp_item in zone_metadata:
                        if "=" not in temp_item:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} "
                                "Zone metadata must like "
                                "this: [<key_metadata>=<value_metadata>]"
                            )
                        meta_key, meta_value = temp_item.split("=")
                        if len(temp_item.split("=")) != 2:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} Metadata must "
                                "be [meta_data=value]"
                            )
                        metadata_dict.update({meta_key: meta_value})

                    if not self._check_key_metadata(list(metadata_dict.keys())):
                        raise ParseError(
                            f"{map_path}: "
                            f"Line {line} "
                            "metadata key must be "
                            "'zone', 'color' or 'max_drones'"
                        )

                    self._sotck_zones(
                        line,
                        key,
                        basedata,
                        metadata_dict,
                        exists_name,
                        coords,
                        coords_set,
                        map_path,
                        width,
                        height
                    )

                elif key == "connection":
                    if self.nb_drones <= 0:
                        raise ParseError(
                            "<nb_drones> must be "
                            "the top of the map file"
                        )

                    connect_data = value.split("[")

                    test_brackets_connection = value.split(" ")
                    if len(test_brackets_connection) == 3:
                        if len(value.split("[")) != 2:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} Each line must be "
                                "separated by one space"
                            )
                    elif len(test_brackets_connection) == 2:
                        if len(value.split("[")) != 1:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} Each line must be "
                                "separated by one space"
                            )

                    if len(connect_data) > 2:
                        raise ParseError(
                            f"{map_path}: "
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
                            f"{map_path}: "
                            f"Line {line} "
                            "connection in mapfile must be <zone1>-<zone2> "
                            "[<metadata_key>=<metadata_value>]"
                        )

                    metadata_con: list[str] = []
                    temp_metadata: dict[str, Any] = {}

                    if temp_meta_con:
                        if " " in temp_meta_con:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} "
                                "Metadata conenction must like "
                                "this: [max_link_capacity=<metadata_value>]"
                            )
                        metadata_con = temp_meta_con.split("=")
                        if len(metadata_con) != 2:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} "
                                "connection in mapfile "
                                "must be <zone1>-<zone2> "
                                "[<metadata_key>=<metadata_value>]"
                            )
                        key, value = metadata_con
                        if key != "max_link_capacity" or int(value) <= 0:
                            raise ParseError(
                                f"{map_path}: "
                                f"Line {line} "
                                "For connection metadakey must be "
                                "[max_link_capacity: <metadata_value>] "
                                "(NB: metadata_value > 0)"
                            )
                        try:
                            temp_metadata.update({key: int(value)})
                        except ValueError:
                            raise ParseError(
                                f"{map_path}: "
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
                    start_cpt = 0
                    end_cpt = 0
                    for zone in self.list_zones:
                        if zone.name == z1.strip(" "):
                            zone1 = zone
                            break
                        if zone.is_start:
                            start_cpt += 1
                        if zone.is_end:
                            end_cpt += 1

                    if not zone1.name:
                        raise ParseError(
                            f"{map_path}: Line {line} "
                            "The {z1} is not in zone list"
                        )

                    for zone in self.list_zones:
                        if zone.name == z2.strip(" "):
                            zone2 = zone
                            break

                    if not zone2.name:
                        raise ParseError(
                            f"{map_path}: Line {line} "
                            "The {z2} is not in zone list"
                        )

                    if zone1.name == zone2.name:
                        raise ParseError(
                            f"{map_path}: "
                            f"Line {line} "
                            f"Conenction ({zone1.name},"
                            "{zone2.name}) is not allowed"
                        )

                    connection: Connection = Connection(
                            zone1, zone2, temp_metadata
                        )

                    self.list_connections.append(connection)
