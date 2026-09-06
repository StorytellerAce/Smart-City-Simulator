CREATE TABLE session_features (
    session_id VARCHAR(50) PRIMARY KEY,

    avg_action_intensity DOUBLE PRECISION,
    std_action_intensity DOUBLE PRECISION,

    avg_upgrade_ratio DOUBLE PRECISION,
    avg_demolish_ratio DOUBLE PRECISION,
    avg_build_ratio DOUBLE PRECISION,

avg_build_house_ratio DOUBLE PREpoCISION,
    avg_build_factory_ratio DOUBLE PRECISION,
    avg_build_service_ratio DOUBLE PRECISION,
    avg_build_supply_ratio DOUBLE PRECISION,
    avg_build_road_ratio DOUBLE PRECISION,

    avg_house_per_turn DOUBLE PRECISION,
    avg_factory_per_turn DOUBLE PRECISION,
    avg_service_per_turn DOUBLE PRECISION,
    avg_supply_per_turn DOUBLE PRECISION,
    avg_road_per_turn DOUBLE PRECISION,

    avg_gold_per_population DOUBLE PRECISION,
    avg_tax_per_population DOUBLE PRECISION,
    avg_population_per_ap DOUBLE PRECISION,
    avg_house_per_road DOUBLE PRECISION,

    avg_bad_placement DOUBLE PRECISION,
    avg_no_service DOUBLE PRECISION,
    avg_low_satisfaction DOUBLE PRECISION,

    avg_population_growth DOUBLE PRECISION,
    avg_gold_growth DOUBLE PRECISION,
    avg_supply_growth DOUBLE PRECISION,
    avg_ap_growth DOUBLE PRECISION,
    avg_satisfaction_growth DOUBLE PRECISION,
    avg_service_growth DOUBLE PRECISION,
    avg_pollution_growth DOUBLE PRECISION,
    avg_tax_income_growth DOUBLE PRECISION,

    std_population_growth DOUBLE PRECISION,
    std_gold_growth DOUBLE PRECISION,
    std_supply_growth DOUBLE PRECISION,
    std_satisfaction_growth DOUBLE PRECISION,
    std_service_growth DOUBLE PRECISION,
    std_pollution_growth DOUBLE PRECISION,

    avg_satisfaction_index DOUBLE PRECISION,
    avg_service_index DOUBLE PRECISION,
    avg_pollution_index DOUBLE PRECISION,

    total_population_growth DOUBLE PRECISION,
    total_gold_growth DOUBLE PRECISION,
    total_supply_growth DOUBLE PRECISION,
    total_ap_growth DOUBLE PRECISION,
    total_tax_income_growth DOUBLE PRECISION,

    supply_efficiency DOUBLE PRECISION,
    avg_supply_ratio DOUBLE PRECISION,
    min_supply_ratio DOUBLE PRECISION,

    service_to_house DOUBLE PRECISION,
    factory_to_house DOUBLE PRECISION,

    used_service_early DOUBLE PRECISION,
    used_factory_early DOUBLE PRECISION,

    early_service_ratio DOUBLE PRECISION,
    early_factory_ratio DOUBLE PRECISION,
    early_service_to_house DOUBLE PRECISION,
    early_factory_to_house DOUBLE PRECISION,

    final_turn INTEGER,
    final_gold DOUBLE PRECISION,
    final_population DOUBLE PRECISION,
    final_supply DOUBLE PRECISION,
    final_ap DOUBLE PRECISION,
    final_satisfaction DOUBLE PRECISION,
    final_service DOUBLE PRECISION,
    final_pollution DOUBLE PRECISION,
    final_tax_income DOUBLE PRECISION,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES gameplay_sessions(session_id)
);