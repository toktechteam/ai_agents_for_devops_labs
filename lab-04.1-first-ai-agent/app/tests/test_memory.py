from pathlib import Path

from memory import MemoryManager


def test_memory_manager_works_with_sqlite(tmp_path: Path):
    db_path = tmp_path / "episodes.db"
    mm = MemoryManager(db_path=str(db_path))

    alert = {"type": "high_cpu", "service": "payment-api"}
    mm.remember_working("current_alert", alert)

    eid = mm.record_episode(alert, "success=true, steps=2")
    assert isinstance(eid, int)

    recent = mm.recent_episodes(limit=5)
    assert len(recent) >= 1
    assert recent[0]["id"] == eid
    assert recent[0]["alert_type"] == "high_cpu"
