from datetime import datetime
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base, Family, Event

DATABASE_URL = "sqlite:///family.db"
engine = create_engine("sqlite:///family.db", connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_family(family_id: int, access_token: str, db: Session, events: list = None) -> Family | Exception:
    try:
        family = Family(family_id=family_id, access_token=access_token)
        db.add(family)
        db.commit()

        for event in events:
            create_event(event.name, event.description, family_id, event.date, db)

        return family
    except Exception as e:
        print(e)


def create_event(name: str, description: str, family_id: int, date: datetime.date, db: Session) -> Event | Exception:
    try:
        event = Event(name=name, description=description, date=date, family_id=family_id)
        db.add(event)
        db.commit()
        return event
    except Exception as e:
        print(e)


def family_list(db: Session) -> list[Type[Family]]:
    return db.query(Family).all()


def event_list(db: Session) -> list[Type[Event]]:
    return db.query(Event).all()


def get_events_by_family(family_id: int, db: Session) -> list[Type[Event]] | Exception:
    try:
        return db.query(Event).filter_by(family_id=family_id).all()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
