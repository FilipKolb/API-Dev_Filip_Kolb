from sqlalchemy.orm import Session

import models
import schemas



def get_Person(db: Session, Person_id: int):
    return db.query(models.Person).filter(models.Person.id == Person_id).first()


def get_Person_by_email(db: Session, email: str):
    return db.query(models.Person).filter(models.Person.email == email).first()


def get_Persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()


def create_Person(db: Session, Person: schemas.PersonCreate):
    db_Person = models.Person(email=Person.email, name=Person.name)
    db.add(db_Person)
    db.commit()
    db.refresh(db_Person)
    return db_Person

def delete_person(db: Session, person_id: int):
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()

    if db_person:
        db.delete(db_person)
        db.commit()
        return True  # Indicate successful deletion
    else:
        return False  # Indicate person not found

def get_Gyms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Gym).offset(skip).limit(limit).all()


def create_gym(db: Session, gym: schemas.GymCreate):
    db_gym = models.Gym(name=gym.name, description=gym.description)
    db.add(db_gym)
    db.commit()
    db.refresh(db_gym)
    return db_gym


def assign_Person_to_Gym(db: Session, gym_id: int, Person_id: int):
    db_gym = db.query(models.Gym).filter(models.Gym.id == gym_id).first()
    db_Person = db.query(models.Person).filter(models.Person.id == Person_id).first()

    if not db_gym or not db_Person:
        return None  # Handle not found cases according to your requirements

#TODO: if person.dbgym == db_gym is het FALSE dus de persoon zit al in die gym.

    db_Person.gyms.append(db_gym)
    db.commit()
    db.refresh(db_gym)

    return {"Person": db_Person, "gym": db_gym}



