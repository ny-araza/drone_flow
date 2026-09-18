from typing import Any
from .zone import Zone
from .error import ParseError
from .utils import display_zone

def parse(data: str) -> tuple[int ,list[Zone]]:
    temp: list[str] = data.split("\n")
    list_zones: list[Zone] = []
    nb_drones: int = 0
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
            for val in value.split(" ")[1:4]:
                basedata.append(val)
            for meta_val in value.split(" ")[4:]:
                temp = meta_val.strip("[]")
                if temp:
                    metadata.append(temp)
            if key != "connection":
                metadata_dict: dict[str, Any] = {}
                name, x, y = basedata
                for item in metadata:
                    meta_key, meta_value = item.split("=")
                    if len(item.split("=")) != 2:
                        raise ParseError("Metadata must be [meta_data=value]")
                    metadata_dict.update({
                        meta_key: meta_value
                    })
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
            elif key == "connection":
                connection = basedata

    display_zone(list_zones)

