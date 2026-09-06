import re
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONFIG
# ============================================================

DATA_FOLDER = Path(
    r"C:\UnityProjects\FYP\GameWebAPI\app\ml\Analytics\Data\TurnSnapShots"
)

OUTPUT_CSV = Path(
    r"C:\UnityProjects\FYP\GameWebAPI\app\ml\Analytics\Preprocessed\session_features2.csv"
)


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


# ============================================================
# HELPERS
# ============================================================

def extract_session_id(file_path: Path) -> str:
    """
    Extract session ID from filename.

    Example:
        turn_snapshots_20260401_191909.csv
        -> 20260401_191909
    """

    match = re.search(
        r"turn_snapshots_(\d{8}_\d{6})",
        file_path.stem
    )

    if match:
        return match.group(1)

    return file_path.stem


def safe_divide(numerator, denominator):
    """
    Prevent division by zero by replacing zero denominators with NaN.
    """

    if isinstance(denominator, pd.Series):
        denominator = denominator.replace(0, np.nan)

    elif denominator == 0:
        denominator = np.nan

    return numerator / denominator


# ============================================================
# PREPROCESS ONE SESSION
# ============================================================

def preprocess_session(
    turn_snapshot_path: Path
) -> dict | None:

    print("\n" + "=" * 70)
    print(
        f"Processing session: "
        f"{extract_session_id(turn_snapshot_path)}"
    )
    print(
        f"Turn snapshots: {turn_snapshot_path.name}"
    )
    print("=" * 70)

    try:
        turn_df = pd.read_csv(turn_snapshot_path)

    except Exception as e:
        print(f"[ERROR] Failed to read file: {e}")
        return None


    # ========================================================
    # BASIC VALIDATION
    # ========================================================

    if turn_df.empty:
        print("[WARN] Turn snapshot file is empty. Skipping.")
        return None

    print(f"Turn snapshot rows: {len(turn_df)}")


    # ========================================================
    # REQUIRED COLUMNS
    # ========================================================

    required_columns = [
        "Turn",
        "Gold",
        "Population",
        "TotalSupplyProvided",
        "AP",
        "APUsed",
        "UpgradeCount",
        "DemolishCount",
        "SmallHouseCount",
        "BigHouseCount",
        "SupplyCount",
        "ServiceCount",
        "FactoryCount",
        "RoadCount",
        "AverageSatisfactionIndex",
        "AveragePollutionIndex",
        "AverageServiceIndex",
        "HousesNearFactoryCount",
        "HousesWithoutServiceCount",
        "HousesLowSatisfactionCount",
        "TotalTaxIncome"
    ]

    missing = [
        col
        for col in required_columns
        if col not in turn_df.columns
    ]

    if missing:
        print(f"[WARN] Missing columns: {missing}")
        print("[WARN] Skipping this session.")
        return None


    # ========================================================
    # COPY DATAFRAME
    # ========================================================

    preprocessed_turn_df = turn_df.copy()


    # ========================================================
    # PLAYER ACTIONS / BUILDINGS
    # ========================================================

    preprocessed_turn_df["BuiltHouseCount"] = (
        preprocessed_turn_df["SmallHouseCount"].diff()
        + preprocessed_turn_df["BigHouseCount"].diff()
    )

    preprocessed_turn_df["BuiltFactoryCount"] = (
        preprocessed_turn_df["FactoryCount"].diff()
    )

    preprocessed_turn_df["BuiltRoadCount"] = (
        preprocessed_turn_df["RoadCount"].diff()
    )

    preprocessed_turn_df["BuiltServiceCount"] = (
        preprocessed_turn_df["ServiceCount"].diff()
    )

    preprocessed_turn_df["BuiltSupplyCount"] = (
        preprocessed_turn_df["SupplyCount"].diff()
    )


    preprocessed_turn_df["TotalBuildCount"] = (
        preprocessed_turn_df["BuiltHouseCount"]
        + preprocessed_turn_df["BuiltFactoryCount"]
        + preprocessed_turn_df["BuiltRoadCount"]
        + preprocessed_turn_df["BuiltServiceCount"]
        + preprocessed_turn_df["BuiltSupplyCount"]
    )


    preprocessed_turn_df["TurnActionCount"] = (
        preprocessed_turn_df["UpgradeCount"]
        + preprocessed_turn_df["DemolishCount"]
        + preprocessed_turn_df["BuiltHouseCount"]
        + preprocessed_turn_df["BuiltFactoryCount"]
        + preprocessed_turn_df["BuiltRoadCount"]
        + preprocessed_turn_df["BuiltServiceCount"]
        + preprocessed_turn_df["BuiltSupplyCount"]
    )


    preprocessed_turn_df["ActionCount"] = (
        preprocessed_turn_df["UpgradeCount"]
        + preprocessed_turn_df["DemolishCount"]
    )


    # ========================================================
    # ACTION RATIOS
    # ========================================================

    preprocessed_turn_df["ActionIntensity"] = safe_divide(
        preprocessed_turn_df["APUsed"],
        preprocessed_turn_df["AP"]
    )

    preprocessed_turn_df["UpgradeRatio"] = safe_divide(
        preprocessed_turn_df["UpgradeCount"],
        preprocessed_turn_df["TurnActionCount"]
    )

    preprocessed_turn_df["DemolishRatio"] = safe_divide(
        preprocessed_turn_df["DemolishCount"],
        preprocessed_turn_df["TurnActionCount"]
    )

    preprocessed_turn_df["BuildRatio"] = safe_divide(
        preprocessed_turn_df["TotalBuildCount"],
        preprocessed_turn_df["TurnActionCount"]
    )


    # ========================================================
    # BUILDING RATIOS
    # ========================================================

    preprocessed_turn_df["BuildHouseRatio"] = safe_divide(
        preprocessed_turn_df["BuiltHouseCount"],
        preprocessed_turn_df["TotalBuildCount"]
    )

    preprocessed_turn_df["BuildFactoryRatio"] = safe_divide(
        preprocessed_turn_df["BuiltFactoryCount"],
        preprocessed_turn_df["TotalBuildCount"]
    )

    preprocessed_turn_df["BuildServiceRatio"] = safe_divide(
        preprocessed_turn_df["BuiltServiceCount"],
        preprocessed_turn_df["TotalBuildCount"]
    )

    preprocessed_turn_df["BuildSupplyRatio"] = safe_divide(
        preprocessed_turn_df["BuiltSupplyCount"],
        preprocessed_turn_df["TotalBuildCount"]
    )


    # ========================================================
    # EFFICIENCY FEATURES
    # ========================================================

    preprocessed_turn_df["HousePerRoad"] = safe_divide(
        preprocessed_turn_df["BuiltHouseCount"],
        preprocessed_turn_df["BuiltRoadCount"]
    )

    preprocessed_turn_df["PopulationPerAP"] = safe_divide(
        preprocessed_turn_df["Population"],
        preprocessed_turn_df["APUsed"]
    )

    preprocessed_turn_df["GoldPerPopulation"] = safe_divide(
        preprocessed_turn_df["Gold"],
        preprocessed_turn_df["Population"]
    )

    preprocessed_turn_df["TaxIncomePerPopulation"] = safe_divide(
        preprocessed_turn_df["TotalTaxIncome"],
        preprocessed_turn_df["Population"]
    )


    # ========================================================
    # RISK / MISTAKES
    # ========================================================

    total_houses = (
        preprocessed_turn_df["SmallHouseCount"]
        + preprocessed_turn_df["BigHouseCount"]
    )

    preprocessed_turn_df["BadPlacementRate"] = safe_divide(
        preprocessed_turn_df["HousesNearFactoryCount"],
        total_houses
    )

    preprocessed_turn_df["NoServiceRate"] = safe_divide(
        preprocessed_turn_df["HousesWithoutServiceCount"],
        total_houses
    )

    preprocessed_turn_df["LowSatisfactionRate"] = safe_divide(
        preprocessed_turn_df["HousesLowSatisfactionCount"],
        total_houses
    )


    # ========================================================
    # CLEAN NaN
    # ========================================================

    preprocessed_turn_df.fillna(0, inplace=True)


    # ========================================================
    # AVERAGES
    # ========================================================

    avg_action_intensity = (
        preprocessed_turn_df["ActionIntensity"].mean()
    )

    std_action_intensity = (
        preprocessed_turn_df["ActionIntensity"].std()
    )

    avg_upgrade_ratio = (
        preprocessed_turn_df["UpgradeRatio"].mean()
    )

    avg_demolish_ratio = (
        preprocessed_turn_df["DemolishRatio"].mean()
    )

    avg_build_house_ratio = (
        preprocessed_turn_df["BuildHouseRatio"].mean()
    )

    avg_build_factory_ratio = (
        preprocessed_turn_df["BuildFactoryRatio"].mean()
    )

    avg_build_service_ratio = (
        preprocessed_turn_df["BuildServiceRatio"].mean()
    )

    avg_build_supply_ratio = (
        preprocessed_turn_df["BuildSupplyRatio"].mean()
    )

    avg_gold_per_population = (
        preprocessed_turn_df["GoldPerPopulation"].mean()
    )

    avg_bad_placement = (
        preprocessed_turn_df["BadPlacementRate"].mean()
    )

    avg_no_service = (
        preprocessed_turn_df["NoServiceRate"].mean()
    )


    # ========================================================
    # INDEX / GROWTH
    # ========================================================

    preprocessed_turn_df["PopulationGrowth"] = (
        preprocessed_turn_df["Population"].diff()
    )

    preprocessed_turn_df["GoldGrowth"] = (
        preprocessed_turn_df["Gold"].diff()
    )

    preprocessed_turn_df["APGrowth"] = (
        preprocessed_turn_df["AP"].diff()
    )

    preprocessed_turn_df["SupplyGrowth"] = (
        preprocessed_turn_df["TotalSupplyProvided"].diff()
    )


    avg_population_growth = (
        preprocessed_turn_df["PopulationGrowth"].mean()
    )

    avg_satisfaction_index = (
        preprocessed_turn_df["AverageSatisfactionIndex"].mean()
    )

    avg_service_growth = (
        preprocessed_turn_df["AverageServiceIndex"].diff().mean()
    )

    avg_gold_growth = (
        preprocessed_turn_df["GoldGrowth"].mean()
    )

    avg_supply_growth = (
        preprocessed_turn_df["SupplyGrowth"].mean()
    )


    # ========================================================
    # STANDARD DEVIATION
    # ========================================================

    std_gold_growth = (
        preprocessed_turn_df["GoldGrowth"].std()
    )

    std_population_growth = (
        preprocessed_turn_df["PopulationGrowth"].std()
    )

    std_satisfaction_growth = (
        preprocessed_turn_df["AverageSatisfactionIndex"]
        .diff()
        .std()
    )


    # ========================================================
    # TOTAL GROWTH
    # ========================================================

    total_population_growth = (
        preprocessed_turn_df["Population"].iloc[-1]
        - preprocessed_turn_df["Population"].iloc[0]
    )

    total_gold_growth = (
        preprocessed_turn_df["Gold"].iloc[-1]
        - preprocessed_turn_df["Gold"].iloc[0]
    )

    total_supply_growth = (
        preprocessed_turn_df["TotalSupplyProvided"].iloc[-1]
        - preprocessed_turn_df["TotalSupplyProvided"].iloc[0]
    )

    total_ap_growth = (
        preprocessed_turn_df["AP"].iloc[-1]
        - preprocessed_turn_df["AP"].iloc[0]
    )


    # ========================================================
    # SUPPLY
    # ========================================================

    supply_ratio = safe_divide(
        preprocessed_turn_df["TotalSupplyProvided"],
        preprocessed_turn_df["Population"]
    )

    supply_efficiency = (
        total_supply_growth / total_population_growth
        if total_population_growth != 0
        else 0
    )


    # ========================================================
    # BUILDING AVERAGES
    # ========================================================

    avg_house_per_turn = (
        preprocessed_turn_df["BuiltHouseCount"].mean()
    )

    avg_factory_per_turn = (
        preprocessed_turn_df["BuiltFactoryCount"].mean()
    )


    # ========================================================
    # ONE SESSION = ONE ROW
    # ========================================================

    session_features = {

        "session_id":
            extract_session_id(turn_snapshot_path),

        "avg_action_intensity":
            avg_action_intensity,

        "std_action_intensity":
            std_action_intensity,

        "avg_upgrade_ratio":
            avg_upgrade_ratio,

        "avg_demolish_ratio":
            avg_demolish_ratio,

        "avg_build_house_ratio":
            avg_build_house_ratio,

        "avg_build_factory_ratio":
            avg_build_factory_ratio,

        "avg_build_service_ratio":
            avg_build_service_ratio,

        "avg_build_supply_ratio":
            avg_build_supply_ratio,

        "avg_gold_per_population":
            avg_gold_per_population,

        "avg_bad_placement":
            avg_bad_placement,

        "avg_no_service":
            avg_no_service,

        "avg_population_growth":
            avg_population_growth,

        "avg_satisfaction_index":
            avg_satisfaction_index,

        "avg_service_growth":
            avg_service_growth,

        "avg_gold_growth":
            avg_gold_growth,

        "avg_supply_growth":
            avg_supply_growth,

        "std_gold_growth":
            std_gold_growth,

        "std_population_growth":
            std_population_growth,

        "std_satisfaction_growth":
            std_satisfaction_growth,

        "total_population_growth":
            total_population_growth,

        "total_gold_growth":
            total_gold_growth,

        "total_supply_growth":
            total_supply_growth,

        "total_ap_growth":
            total_ap_growth,

        "supply_efficiency":
            supply_efficiency,

        "avg_house_per_turn":
            avg_house_per_turn,

        "avg_factory_per_turn":
            avg_factory_per_turn
    }


    # ========================================================
    # REPLACE NaN
    # ========================================================

    for key, value in session_features.items():

        if pd.isna(value):
            session_features[key] = 0


    return session_features


# ============================================================
# PROCESS ALL SESSIONS
# ============================================================

def preprocess_all_sessions(
    data_folder: Path,
    output_csv: Path
) -> pd.DataFrame:

    turn_snapshot_files = sorted(
        data_folder.glob("turn_snapshots_*.csv")
    )

    if not turn_snapshot_files:
        raise FileNotFoundError(
            f"No turn_snapshots_*.csv files found in:\n"
            f"{data_folder}"
        )


    all_rows = []


    for turn_snapshot_path in turn_snapshot_files:

        row = preprocess_session(
            turn_snapshot_path
        )

        if row is not None:
            all_rows.append(row)


    if not all_rows:
        raise ValueError(
            "No valid sessions were successfully processed."
        )


    # ========================================================
    # COMBINE
    # ========================================================

    all_features_df = pd.DataFrame(all_rows)


    all_features_df = (
        all_features_df
        .sort_values("session_id")
        .reset_index(drop=True)
    )


    # ========================================================
    # SAVE
    # ========================================================

    output_csv.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    all_features_df.to_csv(
        output_csv,
        index=False
    )


    print("\n" + "=" * 70)
    print("PREPROCESSING COMPLETE")
    print("=" * 70)

    print(
        f"Sessions processed: "
        f"{len(all_features_df)}"
    )

    print(
        f"Output: {output_csv}"
    )

    print(
        f"Shape: {all_features_df.shape}"
    )

    print("\nSession IDs:")

    print(
        all_features_df["session_id"].tolist()
    )


    return all_features_df


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    all_features_df = preprocess_all_sessions(
        DATA_FOLDER,
        OUTPUT_CSV
    )

    print("\n=== Combined Session-Level Features ===")
    print(all_features_df.head())

    print("\nShape:")
    print(all_features_df.shape)