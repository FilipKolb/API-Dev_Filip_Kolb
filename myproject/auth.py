from passlib.context import CryptContext
import crud
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "df0c89a9894a04e6c8c9c79ad7527d701f79469867d1d6164ed7dd30a915409b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_trainer(db: Session, trainer_name: str, password: str):
    print(f"Trainer name: {trainer_name}")
    trainer = crud.get_trainer_by_name(db, trainer_name)
    print(f"Retrieved trainer: {trainer}")
    if not trainer:
        print(f"Trainer with name '{trainer_name}' not found during authentication.")
        return False
    if not verify_password(password, trainer.hashed_password):
        print(f"Password verification failed for trainer '{trainer_name}'")
        return False
    print("Authenticated trainer: True")
    return trainer


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 15 minutes of expiration time if ACCESS_TOKEN_EXPIRE_MINUTES variable is empty
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Adding the JWT expiration time case
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt