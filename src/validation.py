from pydantic import BaseModel, Field, model_validator, ValidationError
from .zone import TypeZone, ColorType

class ZoneValidation(BaseModel):
    name: str = Field(...)
    x: int = Field(...)
    y: int = Field(...)
    is_start: bool = Field(default=False)
    is_end: bool = Field(default=False)
    type: TypeZone = Field(default=TypeZone.NORMAL)
    color: ColorType = Field(default=ColorType.WHITE)
    max_drones: int = Field(default=1)

    @model_validator(mode='after')
    def validation(self) -> "ZoneValidation":
        forbidden_charactere = "-\n\t\a\b\v\f\r:"
        for char in forbidden_charactere:
            if char in self.name:
                raise ValueError(
                    f"Zone name shouldn't contain '-\\n\\t\\a\\b\\v\\f\\r'"
                )
