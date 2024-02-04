from sqlalchemy.orm import DeclarativeBase, relationship, Relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, BigInteger, INTEGER

from dataclasses import dataclass


class Base(DeclarativeBase):

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        s = str()
        for column in self.__table__.columns:
            s += f"{column.name} : {getattr(self, column.name)}\n"
        return s


class Family(Base):
    __tablename__ = "families"

    family_id = Column(INTEGER, primary_key=True)
    access_token = Column(String)
    events = relationship("Event", back_populates="family")


class Event(Base):
    __tablename__ = "events"

    id = Column(INTEGER, autoincrement=True, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    date = Column(Date)
    family_id = Column(Integer, ForeignKey("families.family_id"))
    family = relationship("Family", back_populates="events")

    def as_pretty_string(self):
        return f"🖋 {self.name} 🖋\n\n📅 {self.date.strftime('%d.%m.%Y')} 📅"
