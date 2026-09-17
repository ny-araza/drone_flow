from typing import Any
from .zone import Zone
from .error import ParseError

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
            for val in value.split(" ")[1:]:
                if val.startswith("[") or val.endswith("]"):
                    metadata.append(val.strip("[]"))
                    continue
                basedata.append(val)
            if key != "connection":
                metadata_dict: list[dict[str, Any]] = []
                name, x, y = basedata
                for item in metadata:
                    meta_key, meta_value = item.split("=")
                    if len(item.split("=")) != 2:
                        raise ParseError("Metadata must be [meta_data=value]")
                    metadata_dict.append({
                        meta_key: meta_value
                    })
                print(metadata_dict)
                if key == "start_hub":
                    list_zones.append(
                        Zone(
                                name,
                                x,
                                y,
                                is_start=True,
                                is_end=False,
                                
                            ) 
                    )
                elif key == "end_hub":
                    list_zones.append(
                        Zone(
                                name,
                                x,
                                y,
                                is_start=True,
                                is_end=False,
                            ) 
                    )
            elif key == "connection":
                connection = basedata
