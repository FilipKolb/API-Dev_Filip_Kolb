from pydantic import BaseModel


class GymBase(BaseModel):
    name: str
    location: str


class GymCreate(GymBase):
    pass


class Gym(GymBase):
    id: int

    class Config:
        orm_mode = True


class PersonBase(BaseModel):
    name: str
    email: str


class PersonCreate(PersonBase):
    pass


class Person(PersonBase):
    id: int
    is_active: bool
    Gyms: list[Gym] = []

    class Config:
        orm_mode = True


class PersonGymAssignment(BaseModel):
    Person: Person
    gym: Gym
