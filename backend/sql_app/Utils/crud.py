# In this file we will have reusable functions to interact with the data in the database.

from sqlalchemy.orm import Session
import bcrypt

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    # util for creating a user. expecting email, username, password
    salt = bcrypt.gensalt(rounds=12)
    fake_hashed_password = bcrypt.hashpw(user.password,salt)
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, username=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
