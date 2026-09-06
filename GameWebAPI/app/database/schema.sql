DROP TABLE IF EXISTS turn_snapshots CASCADE;
DROP TABLE IF EXISTS gameplay_sessions CASCADE;

CREATE TABLE gameplay_sessions (
    session_id UUID PRIMARY KEY,
    player_id TEXT NOT NULL,
    started_at_utc TIMESTAMP NOT NULL
);

CREATE TABLE turn_snapshots (
    id SERIAL PRIMARY KEY,

    session_id UUID NOT NULL REFERENCES gameplay_sessions(session_id),

    turn INTEGER NOT NULL,

    gold INTEGER NOT NULL,
    population INTEGER NOT NULL,
    total_supply_provided INTEGER NOT NULL,

    ap INTEGER NOT NULL,
    ap_used INTEGER NOT NULL,

    upgrade_count INTEGER NOT NULL,
    demolish_count INTEGER NOT NULL,

    small_house_count INTEGER NOT NULL,
    big_house_count INTEGER NOT NULL,

    supply_count INTEGER NOT NULL,
    service_count INTEGER NOT NULL,
    factory_count INTEGER NOT NULL,
    road_count INTEGER NOT NULL,

    average_satisfaction_index DOUBLE PRECISION,
    min_satisfaction_index DOUBLE PRECISION,
    max_satisfaction_index DOUBLE PRECISION,

    average_pollution_index DOUBLE PRECISION,
    min_pollution_index DOUBLE PRECISION,
    max_pollution_index DOUBLE PRECISION,

    average_service_index DOUBLE PRECISION,
    min_service_index DOUBLE PRECISION,
    max_service_index DOUBLE PRECISION,

    houses_near_factory_count INTEGER,
    houses_without_service_count INTEGER,
    houses_low_satisfaction_count INTEGER,

    total_tax_income DOUBLE PRECISION
);

CREATE INDEX idx_turn_session
ON turn_snapshots(session_id);

CREATE INDEX idx_turn_number
ON turn_snapshots(turn);