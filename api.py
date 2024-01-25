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
    family_id: int
    access_token: str
    events: list[ApiEvent] = None


@app.post("/families/create")
def post_family(family: ApiFamily, db: Session = Depends(get_db)):
    print(str(family))
    family = create_family(family_id=family.family_id, access_token=family.access_token, events=family.events, db=db)
    return family.as_dict() if family is not None else None


@app.post("/events/create")
def post_event(event: ApiEvent, db: Session = Depends(get_db)):
    return create_event(event.name, event.description, event.family_id, event.date, db).as_dict()


@app.get("/families")
async def get_family_list(db: Session = Depends(get_db)):
    fl = family_list(db)
    return [f.as_dict() for f in fl] if len(fl) else None


@app.get("/events")
async def get_events_list(db: Session = Depends(get_db)):
    el = event_list(db)
    return [f.as_dict() for f in el] if len(el) else None
