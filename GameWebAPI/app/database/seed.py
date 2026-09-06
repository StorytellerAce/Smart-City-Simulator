import uuid
from datetime import datetime

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.postgre_service import PostgresService
from app.models.dto import TurnSnapshotDto
from app.models.TurnActionSummaryDto import TurnActionSummaryDto

from dotenv import load_dotenv

load_dotenv()

postgres = PostgresService()

session_id = str(uuid.uuid4())

postgres.save_session({
    "session_id": session_id,
    "player_id": "Seed_Player",
    "started_at_utc": datetime.utcnow()
})

for turn in range(1, 51):

    snapshot = TurnSnapshotDto(

        turn=turn,

        gold=500 + turn * 75,

        population=20 + turn * 18,

        total_supply_provided=120,

        ap=5,

        ap_used=3,

        upgrade_count=max(0, turn // 5),

        demolish_count=0,

        small_house_count=turn * 2,

        big_house_count=max(0, turn - 10),

        supply_count=3,

        service_count=2,

        factory_count=1 + turn // 10,

        road_count=turn * 6,

        average_satisfaction_index=80 - turn * 0.2,

        average_pollution_index=10 + turn * 0.3,

        average_service_index=78,

        houses_near_factory_count=turn // 6,

        houses_without_service_count=max(0, 5 - turn // 10),

        houses_low_satisfaction_count=turn // 12,

        total_tax_income=250 + turn * 45
    )

    summary = TurnActionSummaryDto(
        turn=turn,
        actions_taken=0,
        buildings_placed=[],
        upgrades=[],
        demolitions=[]
    )

    postgres.save_turn_data(
        session_id=session_id,
        snapshot=snapshot,
        summary=summary
    )

print(f"Created session {session_id}")