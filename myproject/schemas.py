from pydantic import BaseModel


class PokemonBase(BaseModel):
    name: str
    level: int
    type: str


class PokemonCreate(PokemonBase):
    pass


class PokemonUpdateLevel(BaseModel):
    level: int


class Pokemon(PokemonBase):
    id: int

    class Config:
        orm_mode = True

class TrainerBase(BaseModel):
    name: str

class TrainerCreate(TrainerBase):
    password: str

class TrainerResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Trainer(TrainerBase):
    id: int

    class Config:
        orm_mode = True