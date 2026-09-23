from typing import Any
from .zone import Zone
from .validation import ZoneValidation
from .error import ParseError
from pydantic import ValidationError
from .connection import Connection


def check_unique_zone_name(
        name: str, 
        zones_name: list[str]
        ) -> list[str]:
    if name in zones_name:
        return []
    zones_name.append(name)
    return zones_name

def validate_zone(
        name: str,
        x: int,
        y: int,
        metadata_dict: dict[str, Any]
) -> bool:
    try:
        ZoneValidation(
            name=name,
            x=x,
            y=y,
            is_start=True,
            is_end=False,
            max_drones=metadata_dict.get("max_drones", 1),
            color=metadata_dict.get("color", "white"),
            type=metadata_dict.get("zone", "normal")
        )
        return True
    except ValidationError as e:
        for error in e.errors():
            raise ParseError(f"{error["msg"]}")
        return False

def sotck_zones(
        key: str, 
        list_zones: list[Zone],
        basedata: list[str],
        metadata_dict: dict[str, Any],
        exists_name: list[str]
        ) -> list[Zone]:
    name, x, y = basedata
    if check_unique_zone_name(name, exists_name):
        if validate_zone(
            name, x, y, metadata_dict
        ):
            if key == "start_hub":
                list_zones.append(
                    Zone(
                            name,
                            x,
                            y,
                            is_start=True,
                            is_end=False,
                            max_drones=metadata_dict.get("max_drones", 1),
                            color=metadata_dict.get("color", "black"),
                            type=metadata_dict.get("zone", "normal")
                        ) 
                )
            elif key == "end_hub":
                list_zones.append(
                    Zone(
                            name,
                            x,
                            y,
                            is_start=False,
                            is_end=True,
                            max_drones=metadata_dict.get("max_drones", 1),
                            color=metadata_dict.get("color", "black"),
                            type=metadata_dict.get("zone", "normal"),
                        ) 
                )
            else:
                list_zones.append(
                    Zone(
                            name,
                            x,
                            y,
                            is_start=False,
                            is_end=False,
                            max_drones=metadata_dict.get("max_drones", 1),
                            color=metadata_dict.get("color", "black"),
                            type=metadata_dict.get("zone", "normal"),
                        ) 
                )
    else:
        raise ParseError(f"{name} is not an unique zone name")
    return list_zones

def check_key_metadata(keys: list[str]) -> bool:
    all_key_metadata: list[str] = [
        "zone", "color", "max_drones"
    ]
    for key in keys:
        if not key in all_key_metadata:
            return False
    return True

def parse(data: str) -> tuple[int ,list[Zone]]:
    if not ("start_hub" in data and "end_hub" in data):
        raise ParseError("map file must contain 'start_hub' and 'end_hub'")
    temp: list[str] = data.split("\n")
    list_zones: list[Zone] = []
    list_connections: list[Connection] = []
    nb_drones: int = 0
    exists_name: list[str] = []
    for tmp in temp:
        if not tmp.startswith("#") and tmp:
            item = tmp.split(":")
            if len(item) != 2:
                raise ParseError(
                    "One single ':' per line must " \
                    "be present in the map file"
                )
            key, value = item
            if key == "nb_drones" :
                try:
                    nb_drones = int(value)
                    if nb_drones < 0:
                        raise ParseError(
                            "'nb_drones' must be " \
                            "int and positive"
                            )
                    continue
                except ValueError:
                    nb_drones = 0
                    raise ParseError(
                        "'nb_drones' must be " \
                        "int and positive"
                        )
            metadata: list[str] = []
            basedata: list[str] = []
            if key != "connection":
                temp_value = value.split("[")
                basedata = temp_value[0].strip(" ").split(" ")
                if len(basedata) != 3:
                    raise ParseError(
                        "An error occured on map file line: " \
                        "line must be: <type_zone>: <zone_name> <pos_x> <pos_y> " \
                        "[<metadata_key>=<metadata_value>]"
                        )
                for meta_val in temp_value[1].split(" "):
                    temp = meta_val.strip("[]")
                    if temp:
                        metadata.append(temp)
                metadata_dict: dict[str, Any] = {}

                for item in metadata:
                    meta_key, meta_value = item.split("=")
                    if len(item.split("=")) != 2:
                        raise ParseError("Metadata must be [meta_data=value]")
                    metadata_dict.update({
                        meta_key: meta_value
                })
                if not check_key_metadata(list(metadata_dict.keys())):
                    raise ParseError("metadata key must be 'zone'" \
                            ", 'color' or 'max_drones'")
                list_zones = sotck_zones(
                    key, 
                    list_zones, 
                    basedata, 
                    metadata_dict,
                    exists_name
                    )
            elif key == "connection":
                connect_data = value.split("[")
                if len(connect_data) > 2:
                    raise ParseError(
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
                        "connection in mapfile must be <zone1>-<zone2> "
                        "[<metadata_key>=<metadata_value>]"
                        )
                
                metadata_con = ""
                metadata: dict[str, Any] = {}
                if temp_meta_con:
                    metadata_con = temp_meta_con.split("=")
                    if len(metadata_con) != 2:
                        raise ParseError(
                            "connection in mapfile must be <zone1>-<zone2> "
                            "[<metadata_key>=<metadata_value>]"
                            )
                    key, value = metadata_con
                    if key != "max_link_capacity" or int(value) <= 0:
                        raise ParseError(
                            "For connection metadakey must be "
                            "[max_link_capacity: <metadata_value>] "
                            "(NB: metadata_value > 0)"
                            )
                    try:
                        metadata.update({
                            key: int(value)
                        })
                    except ValueError:
                        raise ParseError(
                            "In connection: metadata_value must be > 0 and numbers"
                            )
                zone1: Zone = Zone(
                    name="",
                    color="",
                    is_end=False,
                    is_start=False,
                    max_drones=1,
                    type="normal",
                    x=0,
                    y=0,
                )
                zone2: Zone = Zone(
                    name="",
                    color="",
                    is_end=False,
                    is_start=False,
                    max_drones=1,
                    type="normal",
                    x=0,
                    y=0,
                )
                for zone in list_zones:
                    if zone.name == basedata_con[0].strip(" "):
                        zone1 = zone
                        break
                for zone in list_zones:
                    if zone.name == basedata_con[1].strip(" "):
                        zone2 = zone
                        break
                connection: Connection = Connection(zone1, zone2, metadata)
                list_connections.append(connection)
    for conn in list_connections:
        print(f"{conn.zone1.name}-{conn.zone2.name} [{conn.metadata}]")
