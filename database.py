from datetime import datetime
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base, Family, Event

import logging

DATABASE_URL = "sqlite:///family.db"
engine = create_engine("sqlite:///family.db", pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_family_by_id(family_id: int, db: Session) -> Type[Family]:
    try:
        return db.query(Family).get(family_id)
    except Exception as e:
        db.rollback()
        logging.error(e)


def delete_old_family(family_id: int, db: Session):
    try:
        events = db.query(Event).filter_by(family_id=family_id)
        for event in events:
            db.delete(event)
        family = db.query(Family).filter_by(family_id=family_id).all()[0]
        db.delete(family)
    except Exception as e:
        db.rollback()
        logging.error(e)


def create_family(family_id: int, access_token: str, db: Session, events: list = None) -> Family | Exception:
    try:
        delete_old_family(family_id, db)

        family = Family(family_id=family_id, access_token=access_token)
        db.add(family)
        db.commit()

        for event in events:
            create_event(event.name, event.description, family_id, event.date, db)

        return family
    except Exception as e:
        db.rollback()
        logging.error(e)


def create_event(name: str, description: str, family_id: int, date: datetime.date, db: Session) -> Event | Exception:
    try:
        logging.info(f"New event with date: {date}")
        event = Event(name=name, description=description, date=date, family_id=family_id)
        db.add(event)
        db.commit()
        return event
    except Exception as e:
        db.rollback()
        logging.error(e)


def family_list(db: Session) -> list[Type[Family]]:
    try:
        return db.query(Family).all()
    except Exception as e:
        db.rollback()
        logging.error(e)


def event_list(db: Session) -> list[Type[Event]]:
    try:
        return db.query(Event).all()
    except Exception as e:
        db.rollback()
        logging.error(e)


def get_events_by_family(family_id: int, db: Session) -> list[Type[Event]] | Exception:
    try:
        return db.query(Event).filter_by(family_id=family_id).all()
    except Exception as e:
        db.rollback()
        logging.error(e)


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
