import json

from datetime import datetime

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from database import *
from models import *


app = FastAPI()


class ApiEvent(BaseModel):
    name: str
    description: str = None
    date: datetime
    family_id: int = None


class ApiFamily(BaseModel):
    telegram_id: int
    events: list[ApiEvent] = None


@app.post("/families/create")
def post_family(family: ApiFamily, db: Session = Depends(get_db)):
    return create_family(telegram_id=family.telegram_id, events=family.events, db=db).as_dict()


@app.post("/events/create")
def post_event(event: ApiEvent, db: Session = Depends(get_db)):
    return create_event(event.name, event.description, event.family_id, event.date, db).as_dict()


@app.get("/families")
async def get_family_list(db: Session = Depends(get_db)):
    return [f.as_dict() for f in family_list(db)]


@app.get("/events")
async def get_events_list(db: Session = Depends(get_db)):
    return [e.as_dict() for e in event_list(db)]
