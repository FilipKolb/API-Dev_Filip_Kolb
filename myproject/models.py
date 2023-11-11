from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Person(Base):
    __tablename__ = "Persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    gyms = relationship("Gym", back_populates="member")


class Gym(Base):
    __tablename__ = "Gyms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    member_id = Column(Integer, ForeignKey("Persons.id"))

    member = relationship("Person", back_populates="gyms")
