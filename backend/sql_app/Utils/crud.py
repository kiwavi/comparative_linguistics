# In this file we will have reusable functions to interact with the data in the database.

from sqlalchemy.orm import Session
import bcrypt
import json
from email_validator import validate_email, EmailNotValidError

from . import models, schemas

def ValidateMail(email):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        email = emailinfo.normalized
    except EmailNotValidError as e:
        print(str(e))

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    # util for creating a user. email, username, password
    if (validate_email(user.email)):
        salt = bcrypt.gensalt(rounds=12)
        password_bytes = user.password.encode('utf-8') 
        hashed_password = bcrypt.hashpw(password_bytes,salt) # postpone due to some error
        db_user = models.User(email=user.email, hashed_password=hashed_password, username=user.username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # print(type(db_user))
        return db_user

def get_user_by_email(db: Session, email: str):
    # util for fetching user via email
    return db.query(models.User).filter(models.User.email == email).first()
