import psycopg2
from psycopg2.extras import Json
from app.models.dto import TurnSnapshotDto
from app.models.TurnActionSummaryDto import TurnActionSummaryDto


class PostgresService:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="teoh0628",
            port=5432
        )

    def save_session(self, session: dict):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO gameplay_sessions (
                    session_id,
                    player_id,
                    started_at_utc
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (session_id) DO NOTHING;
            """, (
                session["session_id"],
                session["player_id"],
                session["started_at_utc"]
            ))

        self.conn.commit()

    def save_turn_snapshot(self, session_id: str, snapshot: TurnSnapshotDto):
        if isinstance(snapshot, dict):
            snapshot = TurnSnapshotDto(**self.unity_snapshot_to_snake(snapshot))

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO turn_snapshots (
                    session_id,
                    turn,
                    gold,
                    population,
                    total_supply_provided,
                    ap,
                    ap_used,
                    upgrade_count,
                    demolish_count,
                    small_house_count,
                    big_house_count,
                    supply_count,
                    service_count,
                    factory_count,
                    road_count,
                    average_satisfaction_index,
                    average_pollution_index,
                    average_service_index,
                    houses_near_factory_count,
                    houses_without_service_count,
                    houses_low_satisfaction_count,
                    total_tax_income
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                );
            """, (
                session_id,
                snapshot.turn,
                snapshot.gold,
                snapshot.population,
                snapshot.total_supply_provided,
                snapshot.ap,
                snapshot.ap_used,
                snapshot.upgrade_count,
                snapshot.demolish_count,
                snapshot.small_house_count,
                snapshot.big_house_count,
                snapshot.supply_count,
                snapshot.service_count,
                snapshot.factory_count,
                snapshot.road_count,
                snapshot.average_satisfaction_index,
                snapshot.average_pollution_index,
                snapshot.average_service_index,
                snapshot.houses_near_factory_count,
                snapshot.houses_without_service_count,
                snapshot.houses_low_satisfaction_count,
                snapshot.total_tax_income
            ))

        self.conn.commit()

    # def save_turn_action_summary(
    #     self,
    #     session_id: str,
    #     summary: TurnActionSummaryDto
    # ):
    #     if isinstance(summary, dict):
    #         summary = TurnActionSummaryDto(**self.unity_summary_to_snake(summary))

    #     with self.conn.cursor() as cur:
    #         cur.execute("""
    #             INSERT INTO turn_action_summaries (
    #                 session_id,
    #                 turn,
    #                 actions_taken,
    #                 buildings_placed,
    #                 upgrades,
    #                 demolitions
    #             )
    #             VALUES (%s, %s, %s, %s, %s, %s);
    #         """, (
    #             session_id,
    #             summary.turn,
    #             summary.actions_taken,
    #             Json([item.model_dump() for item in summary.buildings_placed]),
    #             Json([item.model_dump() for item in summary.upgrades]),
    #             Json([item.model_dump() for item in summary.demolitions])
    #         ))

    #     self.conn.commit()

    def save_turn_data(
        self,
        session_id: str,
        snapshot: TurnSnapshotDto,
        summary: TurnActionSummaryDto
    ):
        self.save_turn_snapshot(session_id, snapshot)
        # self.save_turn_action_summary(session_id, summary)

    def unity_snapshot_to_snake(self, data: dict) -> dict:
        return {
            "turn": data["Turn"],
            "gold": data["Gold"],
            "population": data["Population"],
            "total_supply_provided": data["TotalSupplyProvided"],
            "ap": data["AP"],
            "ap_used": data["APUsed"],
            "upgrade_count": data["UpgradeCount"],
            "demolish_count": data["DemolishCount"],

            "small_house_count": data["SmallHouseCount"],
            "big_house_count": data["BigHouseCount"],
            "supply_count": data["SupplyCount"],
            "service_count": data["ServiceCount"],
            "factory_count": data["FactoryCount"],
            "road_count": data["RoadCount"],

            "average_satisfaction_index": data["AverageSatisfactionIndex"],
            "average_pollution_index": data["AveragePollutionIndex"],
            "average_service_index": data["AverageServiceIndex"],

            "houses_near_factory_count": data["HousesNearFactoryCount"],
            "houses_without_service_count": data["HousesWithoutServiceCount"],
            "houses_low_satisfaction_count": data["HousesLowSatisfactionCount"],

            "total_tax_income": data["TotalTaxIncome"],
        }

    def unity_summary_to_snake(self, data: dict) -> dict:
        return {
            "turn": data["Turn"],
            "actions_taken": data["ActionsTaken"],
            "buildings_placed": [
                {
                    "building_type": x["building_type"] if "building_type" in x else x["BuildingType"],
                    "position": {
                        "x": x["position"]["x"] if "position" in x else x["Position"]["x"],
                        "y": x["position"]["y"] if "position" in x else x["Position"]["y"]
                    }
                }
                for x in data.get("BuildingsPlaced", [])
            ],
            "upgrades": [
                {
                    "building_type": x.get("building_type", x["BuildingType"]),
                    "position": {
                        "x": x.get("position", x["Position"])["x"],
                        "y": x.get("position", x["Position"])["y"]
                    },
                    "from_level": x.get("from_level", x["FromLevel"]),
                    "to_level": x.get("to_level", x["ToLevel"])
                }
                for x in data.get("Upgrades", [])
            ],
            "demolitions": [
                {
                    "building_type": x.get("building_type", x["BuildingType"]),
                    "position": {
                        "x": x.get("position", x["Position"])["x"],
                        "y": x.get("position", x["Position"])["y"]
                    }
                }
                for x in data.get("Demolitions", [])
            ]
        }

    def save_session_features(self, features: dict):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO session_features (
                    session_id,

                    avg_action_intensity,
                    std_action_intensity,

                    avg_upgrade_ratio,
                    avg_demolish_ratio,
                    avg_build_ratio,

                    avg_build_house_ratio,
                    avg_build_factory_ratio,
                    avg_build_service_ratio,
                    avg_build_supply_ratio,
                    avg_build_road_ratio,

                    avg_house_per_turn,
                    avg_factory_per_turn,
                    avg_service_per_turn,
                    avg_supply_per_turn,
                    avg_road_per_turn,

                    avg_gold_per_population,
                    avg_tax_per_population,
                    avg_population_per_ap,
                    avg_house_per_road,

                    avg_bad_placement,
                    avg_no_service,
                    avg_low_satisfaction,

                    avg_population_growth,
                    avg_gold_growth,
                    avg_supply_growth,
                    avg_ap_growth,
                    avg_satisfaction_growth,
                    avg_service_growth,
                    avg_pollution_growth,
                    avg_tax_income_growth,

                    std_population_growth,
                    std_gold_growth,
                    std_supply_growth,
                    std_satisfaction_growth,
                    std_service_growth,
                    std_pollution_growth,

                    avg_satisfaction_index,
                    avg_service_index,
                    avg_pollution_index,

                    total_population_growth,
                    total_gold_growth,
                    total_supply_growth,
                    total_ap_growth,
                    total_tax_income_growth,

                    supply_efficiency,
                    avg_supply_ratio,
                    min_supply_ratio,

                    service_to_house,
                    factory_to_house,

                    used_service_early,
                    used_factory_early,

                    early_service_ratio,
                    early_factory_ratio,
                    early_service_to_house,
                    early_factory_to_house,

                    final_turn,
                    final_gold,
                    final_population,
                    final_supply,
                    final_ap,
                    final_satisfaction,
                    final_service,
                    final_pollution,
                    final_tax_income
                )
                VALUES (
                    %s,
                    %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (session_id)
                DO UPDATE SET
                    avg_action_intensity = EXCLUDED.avg_action_intensity,
                    std_action_intensity = EXCLUDED.std_action_intensity,

                    avg_upgrade_ratio = EXCLUDED.avg_upgrade_ratio,
                    avg_demolish_ratio = EXCLUDED.avg_demolish_ratio,
                    avg_build_ratio = EXCLUDED.avg_build_ratio,

                    avg_build_house_ratio = EXCLUDED.avg_build_house_ratio,
                    avg_build_factory_ratio = EXCLUDED.avg_build_factory_ratio,
                    avg_build_service_ratio = EXCLUDED.avg_build_service_ratio,
                    avg_build_supply_ratio = EXCLUDED.avg_build_supply_ratio,
                    avg_build_road_ratio = EXCLUDED.avg_build_road_ratio,

                    avg_house_per_turn = EXCLUDED.avg_house_per_turn,
                    avg_factory_per_turn = EXCLUDED.avg_factory_per_turn,
                    avg_service_per_turn = EXCLUDED.avg_service_per_turn,
                    avg_supply_per_turn = EXCLUDED.avg_supply_per_turn,
                    avg_road_per_turn = EXCLUDED.avg_road_per_turn,

                    avg_gold_per_population = EXCLUDED.avg_gold_per_population,
                    avg_tax_per_population = EXCLUDED.avg_tax_per_population,
                    avg_population_per_ap = EXCLUDED.avg_population_per_ap,
                    avg_house_per_road = EXCLUDED.avg_house_per_road,

                    avg_bad_placement = EXCLUDED.avg_bad_placement,
                    avg_no_service = EXCLUDED.avg_no_service,
                    avg_low_satisfaction = EXCLUDED.avg_low_satisfaction,

                    avg_population_growth = EXCLUDED.avg_population_growth,
                    avg_gold_growth = EXCLUDED.avg_gold_growth,
                    avg_supply_growth = EXCLUDED.avg_supply_growth,
                    avg_ap_growth = EXCLUDED.avg_ap_growth,
                    avg_satisfaction_growth = EXCLUDED.avg_satisfaction_growth,
                    avg_service_growth = EXCLUDED.avg_service_growth,
                    avg_pollution_growth = EXCLUDED.avg_pollution_growth,
                    avg_tax_income_growth = EXCLUDED.avg_tax_income_growth,

                    std_population_growth = EXCLUDED.std_population_growth,
                    std_gold_growth = EXCLUDED.std_gold_growth,
                    std_supply_growth = EXCLUDED.std_supply_growth,
                    std_satisfaction_growth = EXCLUDED.std_satisfaction_growth,
                    std_service_growth = EXCLUDED.std_service_growth,
                    std_pollution_growth = EXCLUDED.std_pollution_growth,

                    avg_satisfaction_index = EXCLUDED.avg_satisfaction_index,
                    avg_service_index = EXCLUDED.avg_service_index,
                    avg_pollution_index = EXCLUDED.avg_pollution_index,

                    total_population_growth = EXCLUDED.total_population_growth,
                    total_gold_growth = EXCLUDED.total_gold_growth,
                    total_supply_growth = EXCLUDED.total_supply_growth,
                    total_ap_growth = EXCLUDED.total_ap_growth,
                    total_tax_income_growth = EXCLUDED.total_tax_income_growth,

                    supply_efficiency = EXCLUDED.supply_efficiency,
                    avg_supply_ratio = EXCLUDED.avg_supply_ratio,
                    min_supply_ratio = EXCLUDED.min_supply_ratio,

                    service_to_house = EXCLUDED.service_to_house,
                    factory_to_house = EXCLUDED.factory_to_house,

                    used_service_early = EXCLUDED.used_service_early,
                    used_factory_early = EXCLUDED.used_factory_early,

                    early_service_ratio = EXCLUDED.early_service_ratio,
                    early_factory_ratio = EXCLUDED.early_factory_ratio,
                    early_service_to_house = EXCLUDED.early_service_to_house,
                    early_factory_to_house = EXCLUDED.early_factory_to_house,

                    final_turn = EXCLUDED.final_turn,
                    final_gold = EXCLUDED.final_gold,
                    final_population = EXCLUDED.final_population,
                    final_supply = EXCLUDED.final_supply,
                    final_ap = EXCLUDED.final_ap,
                    final_satisfaction = EXCLUDED.final_satisfaction,
                    final_service = EXCLUDED.final_service,
                    final_pollution = EXCLUDED.final_pollution,
                    final_tax_income = EXCLUDED.final_tax_income;
            """, (
                features["session_id"],

                features["avg_action_intensity"],
                features["std_action_intensity"],

                features["avg_upgrade_ratio"],
                features["avg_demolish_ratio"],
                features["avg_build_ratio"],

                features["avg_build_house_ratio"],
                features["avg_build_factory_ratio"],
                features["avg_build_service_ratio"],
                features["avg_build_supply_ratio"],
                features["avg_build_road_ratio"],

                features["avg_house_per_turn"],
                features["avg_factory_per_turn"],
                features["avg_service_per_turn"],
                features["avg_supply_per_turn"],
                features["avg_road_per_turn"],

                features["avg_gold_per_population"],
                features["avg_tax_per_population"],
                features["avg_population_per_ap"],
                features["avg_house_per_road"],

                features["avg_bad_placement"],
                features["avg_no_service"],
                features["avg_low_satisfaction"],

                features["avg_population_growth"],
                features["avg_gold_growth"],
                features["avg_supply_growth"],
                features["avg_ap_growth"],
                features["avg_satisfaction_growth"],
                features["avg_service_growth"],
                features["avg_pollution_growth"],
                features["avg_tax_income_growth"],

                features["std_population_growth"],
                features["std_gold_growth"],
                features["std_supply_growth"],
                features["std_satisfaction_growth"],
                features["std_service_growth"],
                features["std_pollution_growth"],

                features["avg_satisfaction_index"],
                features["avg_service_index"],
                features["avg_pollution_index"],

                features["total_population_growth"],
                features["total_gold_growth"],
                features["total_supply_growth"],
                features["total_ap_growth"],
                features["total_tax_income_growth"],

                features["supply_efficiency"],
                features["avg_supply_ratio"],
                features["min_supply_ratio"],

                features["service_to_house"],
                features["factory_to_house"],

                features["used_service_early"],
                features["used_factory_early"],

                features["early_service_ratio"],
                features["early_factory_ratio"],
                features["early_service_to_house"],
                features["early_factory_to_house"],

                features["final_turn"],
                features["final_gold"],
                features["final_population"],
                features["final_supply"],
                features["final_ap"],
                features["final_satisfaction"],
                features["final_service"],
                features["final_pollution"],
                features["final_tax_income"]
            ))

        self.conn.commit()