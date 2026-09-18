from enum import Enum
from pydantic import BaseModel, Field

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
    

class ZoneValidation(BaseModel):
    name: str = Field(...)
    x: int = Field(...)
    y: int = Field(...)
    is_start: bool = Field(default=False)
    is_end: bool = Field(default=False)
    type: TypeZone = Field(default=TypeZone.NORMAL)
    color: ColorType = Field(default=ColorType.WHITE)
    max_drones: int = Field(default=1)

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
