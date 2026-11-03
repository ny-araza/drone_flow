from enum import Enum


class TypeZone(Enum):
    """Represent the possible type that a zone can be

        Attributes:
            NORMAL = "normal"
            BLOCKED = "blocked"
            RESTRICTED = "restricted"
            PRIORITY = "priority"
    """
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class ColorType(Enum):
    """Represent the color possible for a zone

        Attributes:
            RED = "red"
            BLUE = "blue"
            GREEN = "green"
            YELLOW = "yellow"
            WHITE = "white"
            PURPLE = "purple"
            ORANGE = "orange"
            CYAN = "cyan"
            BROWN = "brown"
            LIME = "lime"
            MAGENTA = "magenta"
            GOLD = "gold"
            BLACK = "black"
            MAROON = "maroon"
            DARKRED = "darkred"
            VIOLET = "violet"
            CRIMSON = "crimson"
            RAINBOW = "rainbow"
            GRAY = "gray"
    """
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    WHITE = "white"
    PURPLE = "purple"
    ORANGE = "orange"
    CYAN = "cyan"
    BROWN = "brown"
    LIME = "lime"
    MAGENTA = "magenta"
    GOLD = "gold"
    BLACK = "black"
    MAROON = "maroon"
    DARKRED = "darkred"
    VIOLET = "violet"
    CRIMSON = "crimson"
    RAINBOW = "rainbow"
    GRAY = "gray"


class Zone:
    """Represent the zone

        Attributes:
            x (int): pos x
            y (int): pos y
            is_start (bool): is a start hub
            is_end (bool): is a end hub
            type (TypeZone): the type of the zone
            max_drones (int): the max drone
                that can be in this zone
            color (ColorType): The color of the zone
            image (str): The image path of the drone
    """
    def __init__(
            self, name: str,
            x: int, y: int,
            is_start: bool = False,
            is_end: bool = False,
            type: TypeZone = TypeZone.NORMAL,
            max_drones: int = 1,
            color: ColorType = ColorType.WHITE,
            image: str = ""
            ):
        """Constructor of the Zone class

            Args:
                x (int): pos x
                y (int): pos y
                is_start (bool): is a start hub
                is_end (bool): is a end hub
                type (TypeZone): the type of the zone
                max_drones (int): the max drone
                    that can be in this zone
                color (ColorType): The color of the zone
                image (str): The image path of the drone
        """
        self.name = name
        self.x = x
        self.y = y
        self.is_start = is_start
        self.is_end = is_end
        self.type = type
        self.max_drones = max_drones
        self.color = color
        self.image = image
