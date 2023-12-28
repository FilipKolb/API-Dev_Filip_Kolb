from sqlalchemy.orm import Session

import models
import schemas
import auth


def get_pokemon(db: Session, pokemon_id: int):
    return db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()


def get_pokemon_by_name(db: Session, name: str):
    return db.query(models.Pokemon).filter(models.Pokemon.name == name).first()


def get_pokemons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pokemon).offset(skip).limit(limit).all()


def create_pokemon(db: Session, pokemon: schemas.PokemonCreate):
    db_pokemon = models.Pokemon(name=pokemon.name, level=pokemon.level, type=pokemon.type)
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon


def delete_pokemon(db: Session, pokemon_id: int):
    db_pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()

    if db_pokemon:
        name = db_pokemon.name
        db.delete(db_pokemon)
        db.commit()
        return f"{name} has been removed"  # Indicate successful deletion
    else:
        return "Pokemon not found"  # Indicate Pokemon not found


def update_pokemon_level(db: Session, pokemon_id: int, new_level: int):
    db_pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()

    if db_pokemon:
        db_pokemon.level = new_level
        db.commit()
        db.refresh(db_pokemon)
        return db_pokemon
    else:
        return None  # Handle Pokemon not found case


def create_trainer(db: Session, trainer: schemas.TrainerCreate):
    hashed_password = auth.get_password_hash(trainer.password)
    db_trainer = models.Trainer(name=trainer.name, hashed_password=hashed_password)
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer


def get_trainer(db: Session, trainer_id: int):
    return db.query(models.Trainer).filter(models.Trainer.id == trainer_id).first()

def get_trainer_by_name(db: Session, name: str):
    print(f"Executing SQL query: SELECT * FROM Trainers WHERE name = '{name}'")
    trainer = db.query(models.Trainer).filter(models.Trainer.name == name).first()
    print(f"Retrieved trainer by name '{name}': {trainer}")
    return trainer


def get_trainers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trainer).offset(skip).limit(limit).all()
