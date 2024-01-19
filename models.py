from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey


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

    family_id = Column(Integer, primary_key=True, index=True)
    events = relationship("Event", back_populates="family")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    date = Column(Date)
    family_id = Column(Integer, ForeignKey("families.family_id"))
    family = relationship("Family", back_populates="events")
