# In this file we will have reusable functions to interact with the data in the database.

from sqlalchemy.orm import Session
import bcrypt
import json
from email_validator import validate_email, EmailNotValidError

from . import models, schemas
from fastapi.security import OAuth2PasswordBearer
from typing import Union, Annotated, Optional
from datetime import timedelta, datetime, timezone
from fastapi import Depends
from jose import JWTError, jwt
from decouple import config
from fastapi import HTTPException, status
from sqlalchemy import or_

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def ValidateMail(email):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        email = emailinfo.normalized
    except EmailNotValidError as e:
        print(str(e))

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.username == user_name).first()

def create_user(db: Session, user: schemas.UserCreate):
    # util for creating a user. email, username, password
    if (validate_email(user.email)):
        salt = bcrypt.gensalt(rounds=12)
        password_bytes = user.password.encode('utf-8') 
        hashed_password = bcrypt.hashpw(password_bytes,salt) # postpone due to some error
        db_user = models.User(email=user.email, hashed_password=hashed_password.decode('utf-8'), username=user.username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # print(type(db_user))
        return db_user

def get_user_by_email(db: Session, email: str):
    # util for fetching user via email
    return db.query(models.User).filter(models.User.email == email).first()


def create_language_family(db:Session, family: schemas.LanguageFamilyCreate):
    language_family = models.Language_Families(name=family.name,language_family_description
                                               = family.language_family_description
                                               )
    db.add(language_family)
    db.commit()
    db.refresh(language_family)
    return language_family

def get_language_family(db:Session, name:str):
    return db.query(models.Language_Families).filter(models.Language_Families.name
                                                     == name).first()

def get_language(db:Session, name:str):
    return db.query(models.Languages).filter(models.Languages.name == name).first()

def create_language(db:Session,language:schemas.LanguageCreate):
    language_create = models.Languages(name=language.name,language_description=
                                       language.language_description,
                                       language_family_id=language.language_family_id)
    db.add(language_create)
    db.commit()
    db.refresh(language_create)
    return language_create

def get_word(db:Session,name:str,language_id:int):
    # checks if there exists a word for that language 
    return db.query(models.Words).filter(models.Words.english_word == name,models.Words.language_id == language_id).first()

def create_word(db:Session,word:schemas.WordsCreate):
    new_word = models.Words(english_word=word.english_word,language_word_equivalent=
                            word.language_word_equivalent,language_id=word.language_id,
                            description=word.description,user_id=word.user_id
                            )
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word

def get_wordlist(db:Session,wordlist:str):
    return db.query(models.WordList).filter(models.WordList.word == wordlist).first()

def create_wordlist(db:Session,wordlist:schemas.WordListBase):
    # check if theres a picture and save it
    new_wordlist = models.WordList(word=wordlist.word)
    db.add(new_wordlist)
    db.commit()
    db.refresh(new_wordlist)
    return new_wordlist

def getwordpic(db:Session,wordpicid:id):
    return db.query(models.WordPicture).filter(models.WordPicture.wordlist_id == wordpicid).first()

def create_wordpic(db:Session,wordpic:schemas.WordPictureBase):
    new_pic = models.WordPicture(wordlist_id=wordpic.wordlist_id)
    db.add(new_pic)
    db.commit()
    db.refresh(new_pic)
    return new_pic


def getwordid(db:Session,wordid:int):
    return db.query(models.WordList).filter(models.WordList.id == wordid).first()

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(db:Session,token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user_by_name(db, username)
        return user
    except JWTError:
        raise credentials_exception

def verify_password(plain_text:str, hashed:str):
    name = bcrypt.checkpw(plain_text.encode('utf-8'),hashed)
    return name

def fetch_languages(db:Session):
    languages = db.query(models.Languages).all()
    return languages

def fetch_language_families(db:Session):
    language_families = db.query(models.Language_Families).all()
    return language_families

def fetch_wordlist(db:Session):
    wordlist = db.query(models.WordList).all()
    return wordlist

def user_language(db:Session,userid:int,userlang:int):
    userlang = db.query(models.Languages).filter(models.Languages.id == userlang).first()
    if userlang:
        user = db.query(models.User).filter(models.User.id == userid).first()
        user.user_lang_id = userlang.id
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

def search_word(db:Session,word:str,language: Optional[int]=None, language_family: Optional[int]=None):    
    # return answers to queries
    if language and language_family:
        word = db.query(models.Words).filter(models.Words.english_word == word,models.Words.language_id == language, models.Words.language_fam_id == language_family).all()
    if language and not language_family:
        word = db.query(models.Words).filter(models.Words.english_word == word,models.Words.language_id == language).all()
    if language_family and not language:
        word = db.query(models.Words).filter(models.Words.english_word == word,models.Words.language_fam_id == language_family).all()
    return word


def get_user_words(db:Session,user_id:int):
    print(user_id)
    words = db.query(models.Words).filter(models.Words.user_id==user_id).all()
    return words
