from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import auth
import crud
import models
import schemas
from database import SessionLocal, engine
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/pokemon/", response_model=schemas.Pokemon)
def create_pokemon(pokemon: schemas.PokemonCreate, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon_by_name(db, name=pokemon.name)
    if db_pokemon:
        raise HTTPException(status_code=400, detail="Pokemon name already registered")
    return crud.create_pokemon(db=db, pokemon=pokemon)


@app.get("/pokemon/", response_model=list[schemas.Pokemon])
def read_pokemons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pokemons = crud.get_pokemons(db, skip=skip, limit=limit)
    return pokemons


@app.get("/pokemon/{pokemon_id}", response_model=schemas.Pokemon)
def read_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon(db, pokemon_id=pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return db_pokemon


@app.delete("/pokemon/{pokemon_id}/", response_model=str)
def delete_pokemon_api(pokemon_id: int, db: Session = Depends(get_db)):
    result = crud.delete_pokemon(db, pokemon_id)

    if not result:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    return result


@app.put("/pokemon/{pokemon_id}/level", response_model=schemas.Pokemon)
def update_pokemon_level(pokemon_id: int, level_update: schemas.PokemonUpdateLevel, db: Session = Depends(get_db)):
    updated_pokemon = crud.update_pokemon_level(db=db, pokemon_id=pokemon_id, new_level=level_update.level)

    if updated_pokemon:
        return updated_pokemon
    else:
        raise HTTPException(status_code=404, detail="Pokemon not found")


@app.post("/trainers/", response_model=schemas.Trainer)
def create_trainer(trainer: schemas.TrainerCreate, db: Session = Depends(get_db)):
    print(f"Created trainer: {trainer}")
    return crud.create_trainer(db=db, trainer=trainer)

# Endpoint to get a trainer by ID
@app.get("/trainers/{trainer_id}", response_model=schemas.Trainer)
def read_trainer_by_name(trainer_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_trainer = crud.get_trainer(db, trainer_id)
    if db_trainer is None:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return db_trainer

# Endpoint to get a list of trainers
@app.get("/trainers/", response_model=list[schemas.Trainer])
def read_trainers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    trainers = crud.get_trainers(db, skip=skip, limit=limit)
    return trainers


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"Trying to authenticate with username: {form_data.username} and password: {form_data.password}")
    #Try to authenticate the user
    trainer = auth.authenticate_trainer(db, form_data.username, form_data.password)
    print(f"Authenticated trainer: {trainer}")
    if not trainer:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": trainer.name}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}