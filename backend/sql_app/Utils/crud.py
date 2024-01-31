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
    return db.query(models.Words).filter(models.Words.english_word == name
                                         and models.Words.language_id == language_id 
                                         ).first()

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

def create_wordlist(db:Session,wordlist:schemas.WordListOut):
    # check if theres a picture and save it
    new_wordlist = models.WordList(word=wordlist.word,picture=wordlist.picture)
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
