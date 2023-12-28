from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Pokemon(Base):
    __tablename__ = "Pokemons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    level = Column(Integer)
    type = Column(String, index=True)

    trainer_id = Column(Integer, ForeignKey('Trainers.id'))
    trainer = relationship("Trainer", back_populates="pokemons")

class Trainer(Base):
    __tablename__ = "Trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    pokemons = relationship("Pokemon", back_populates="trainer")

