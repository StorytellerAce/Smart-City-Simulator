from pydantic import BaseModel, Field, ConfigDict
from typing import List

class PointDto(BaseModel):
    x: int = Field(alias="X")
    y: int = Field(alias="Y")

class BuildActionDto(BaseModel):
    building_type: int = Field(alias="BuildingType")
    position: PointDto = Field(alias="Position")

class UpgradeActionDto(BaseModel):
    building_type: int = Field(alias="BuildingType")
    position: PointDto = Field(alias="Position")
    from_level: int = Field(alias="FromLevel")
    to_level: int = Field(alias="ToLevel")

class DemolishActionDto(BaseModel):
    building_type: int = Field(alias="BuildingType")
    position: PointDto = Field(alias="Position")


class TurnActionSummaryDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    turn: int = Field(alias="Turn")
    actions_taken: int = Field(alias="ActionsTaken")

    buildings_placed: List[BuildActionDto] = Field(
        default_factory=list,
        alias="BuildingsPlaced"
    )

    upgrades: List[UpgradeActionDto] = Field(
        default_factory=list,
        alias="Upgrades"
    )

    demolitions: List[DemolishActionDto] = Field(
        default_factory=list,
        alias="Demolitions"
    )