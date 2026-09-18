from typing import Any
from .zone import Zone
from .validation import ZoneValidation
from .error import ParseError
from .utils import display_zone
from pydantic import ValidationError


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
                connection = basedata

    display_zone(list_zones)
