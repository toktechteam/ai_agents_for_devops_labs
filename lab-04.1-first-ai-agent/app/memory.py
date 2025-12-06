from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import Column, Integer, String, Text, create_engine, text
from sqlalchemy.orm import declarative_base, Session

from config import get_settings

Base = declarative_base()


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_type = Column(String(255))
    service = Column(String(255))
    outcome = Column(Text)


class WorkingMemory:
    """
    Simulates "working memory" (short-term) from Chapter 4.
    In production this could be Redis; here it's an in-process dict.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def remember(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def dump(self) -> Dict[str, Any]:
        return dict(self._store)


class EpisodicMemory:
    """
    Simulates "episodic memory" using SQLite (like Postgres-lite for this lab).
    Stores incident episodes with basic details.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        settings = get_settings()
        self.db_path = db_path or settings.sqlite_path
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False, future=True)
        Base.metadata.create_all(self.engine)

    def record_episode(self, alert_type: str, service: str, outcome: str) -> int:
        with Session(self.engine) as session:
            ep = Episode(alert_type=alert_type, service=service, outcome=outcome)
            session.add(ep)
            session.commit()
            session.refresh(ep)
            return ep.id

    def get_recent_episodes(self, limit: int = 5) -> List[Tuple[int, str, str, str]]:
        with Session(self.engine) as session:
            rows = (
                session.query(Episode)
                .order_by(Episode.id.desc())
                .limit(limit)
                .all()
            )
            return [(e.id, e.alert_type, e.service, e.outcome) for e in rows]


class MemoryManager:
    """
    High-level memory manager combining Working + Episodic memory.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory(db_path=db_path)

    def remember_working(self, key: str, value: Any) -> None:
        self.working.remember(key, value)

    def working_snapshot(self) -> Dict[str, Any]:
        return self.working.dump()

    def record_episode(self, alert: Dict[str, Any], outcome: str) -> int:
        alert_type = alert.get("type", "unknown")
        service = alert.get("service", "unknown")
        return self.episodic.record_episode(alert_type, service, outcome)

    def recent_episodes(self, limit: int = 5) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        for ep_id, alert_type, service, outcome in self.episodic.get_recent_episodes(limit):
            items.append(
                {
                    "id": ep_id,
                    "alert_type": alert_type,
                    "service": service,
                    "outcome": outcome,
                }
            )
        return items
