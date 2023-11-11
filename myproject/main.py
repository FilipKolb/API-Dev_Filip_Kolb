from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

# "sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/Persons/", response_model=schemas.Person)
def create_Person(Person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_Person = crud.get_Person_by_email(db, email=Person.email)
    if db_Person:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_Person(db=db, Person=Person)


@app.get("/Persons/", response_model=list[schemas.Person])
def read_Persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    Persons = crud.get_Persons(db, skip=skip, limit=limit)
    return Persons


@app.get("/Persons/{Person_id}", response_model=schemas.Person)
def read_Person(Person_id: int, db: Session = Depends(get_db)):
    db_Person = crud.get_Person(db, Person_id=Person_id)
    if db_Person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_Person



# Gyms

@app.get("/Gyms/", response_model=list[schemas.Gym])
def read_Gyms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    Gyms = crud.get_Gyms(db, skip=skip, limit=limit)
    return Gyms

@app.post("/Gyms/", response_model=schemas.Gym)
def create_Gym(gym: schemas.GymCreate, db: Session = Depends(get_db)):
    return crud.create_gym(db=db, gym=gym)

@app.post("/Gyms/{gym_id}/Persons/{Person_id}/", response_model=schemas.PersonGymAssignment)
def assign_Person_to_Gym(gym_id: int, Person_id: int, db: Session = Depends(get_db)):
    return crud.assign_Person_to_Gym(db=db, gym_id=gym_id, Person_id=Person_id)

@app.delete("/Persons/{person_id}/", response_model=str)
def delete_person_api(person_id: int, db: Session = Depends(get_db)):
    result = crud.delete_person(db, person_id)

    if not result:
        raise HTTPException(status_code=404, detail="Person not found")

    return result
