from pydantic import BaseModel, Field, \
        model_validator
from zone import TypeZone
from typing_extensions import Self


class ZoneValidation(BaseModel):
    """Validation of a zone with pydantic

        Attributes:
            name (str): name of the zone
            x (int): pos x
            y (int): pos y
            is_start (bool): is a start hub
            is_end (bool): is a end hub
            type (TypeZone): type of a zone
            color (ColorType): color of a zone
            max_drones (int): maximum of drone that can
                be in this zone
    """
    name: str = Field(...)
    x: int = Field(...)
    y: int = Field(...)
    is_start: bool = Field(default=False)
    is_end: bool = Field(default=False)
    type: TypeZone = Field(default=TypeZone.NORMAL)
    color: str = Field(...)
    max_drones: int = Field(default=1)

    @model_validator(mode='after')
    def validation(self) -> Self:
        """Check if the zone name have a - or space
        """
        forbidden_charactere = "-\n\t\a\b\v\f\r:"
        for char in forbidden_charactere:
            if char in self.name:
                raise ValueError(
                    "Zone name shouldn't contain '-\\n\\t\\a\\b\\v\\f\\r'"
                )

        return self
