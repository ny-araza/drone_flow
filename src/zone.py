from enum import Enum

class TypeZone(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

class ColorType(Enum):
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
    def __init__(
            self, name: str, 
            x: int, y: int, 
            is_start: bool = False, 
            is_end: bool = False,
            type: TypeZone = TypeZone.NORMAL,
            max_drones: int = 1,
            color: ColorType = ColorType.WHITE  
            ):
        self.name = name
        self.x = x
        self.y = y
        self.is_start = is_start
        self.is_end = is_end
        self.type = type
        self.max_drones = max_drones
        self.color = color
