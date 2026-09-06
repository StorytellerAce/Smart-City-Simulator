from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class StartSessionRequest(BaseModel):
    player_id: str


class StartSessionResponse(BaseModel):
    session_id: str
    started_at_utc: datetime
    message: str


class ActionLogDto(BaseModel):
    turn: int
    time_since_session_start: float
    action_type: str
    building_type: Optional[str] = None
    position_x: int
    position_y: int
    gold_before: int
    gold_after: int
    ap_before: int
    ap_after: int
    was_valid: bool
    notes: Optional[str] = None

class TurnSnapshotDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    turn: int = Field(alias="Turn")
    gold: int = Field(alias="Gold")
    population: int = Field(alias="Population")
    total_supply_provided: int = Field(alias="TotalSupplyProvided")

    ap: int = Field(alias="AP")
    ap_used: int = Field(alias="APUsed")
    upgrade_count: int = Field(alias="UpgradeCount")
    demolish_count: int = Field(alias="DemolishCount")

    small_house_count: int = Field(alias="SmallHouseCount")
    big_house_count: int = Field(alias="BigHouseCount")
    supply_count: int = Field(alias="SupplyCount")
    service_count: int = Field(alias="ServiceCount")
    factory_count: int = Field(alias="FactoryCount")
    road_count: int = Field(alias="RoadCount")

    average_satisfaction_index: float = Field(alias="AverageSatisfactionIndex")
    min_satisfaction_index: float = Field(alias="MinSatisfactionIndex")
    max_satisfaction_index: float = Field(alias="MaxSatisfactionIndex")

    average_pollution_index: float = Field(alias="AveragePollutionIndex")
    min_pollution_index: float = Field(alias="MinPollutionIndex")
    max_pollution_index: float = Field(alias="MaxPollutionIndex")

    average_service_index: float = Field(alias="AverageServiceIndex")
    min_service_index: float = Field(alias="MinServiceIndex")
    max_service_index: float = Field(alias="MaxServiceIndex")

    houses_near_factory_count: int = Field(alias="HousesNearFactoryCount")
    houses_without_service_count: int = Field(alias="HousesWithoutServiceCount")
    houses_low_satisfaction_count: int = Field(alias="HousesLowSatisfactionCount")

    total_tax_income: int = Field(alias="TotalTaxIncome")

class RecommendObjectiveRequest(BaseModel):
    session_id: str

