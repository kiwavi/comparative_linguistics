from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, Request
from sqlalchemy.orm import Session

from Utils import crud, models, schemas
from Utils.database import SessionLocal, engine
import json
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from typing import Optional, Union, Annotated
from wand.image import Image
import base64
from sqlalchemy_imageattach.context import store_context
from sqlalchemy_imageattach.stores.fs import FileSystemStore
import os
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

models.Base.metadata.create_all(bind=engine)

store = FileSystemStore(path='./Utils/images',base_url=os.getcwd() + '/Utils/images')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
ACCESS_TOKEN_EXPIRE_MINUTES = 1

app = FastAPI()

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register",response_model=schemas.UserOut)
def register(user:schemas.UserCreate, db: Session=Depends(get_db)):
    # db_user = crud.get_user_by_email(get_db(),email=user.email)
    print(type(user.password))
    db_user_check = crud.get_user_by_email(db, user.email)
    if db_user_check:
        raise HTTPException(status_code=400,detail='Email already exists')
    db_user = crud.create_user(db,user);
    return db_user

@app.post("/new/language-family",response_model=schemas.LanguageFamilyOut)
def addlanguagefamily(token: Annotated[str, Depends(oauth2_scheme)],family:schemas.LanguageFamilyCreate,db:Session=Depends(get_db)):
    # needs protection. Superuser only
    language_family_check = crud.get_language_family(db, family.name)
    if language_family_check:
        raise HTTPException(status_code=400,detail='Language family exists')
    new_language_family = crud.create_language_family(db,family)
    return new_language_family

@app.post("/new/language",response_model=schemas.LanguagesOut)
def addlanguage(token: Annotated[str, Depends(oauth2_scheme)],language:schemas.LanguageCreate,db:Session=Depends(get_db)):
    # needs protection. Superuser only
    language_check = crud.get_language(db,language.name)
    if language_check:
        raise HTTPException(status_code=400,detail='Language exists')
    new_language = crud.create_language(db,language)
    return new_language

@app.post("/new/word",response_model=schemas.WordsCreate)
def addword(token: Annotated[str, Depends(oauth2_scheme)],word:schemas.WordsCreate,db:Session=Depends(get_db)):
    # needs protection
    word_check = crud.get_word(db,word.english_word,word.language_id)
    if word_check:
        raise HTTPException(status_code=400,detail='The word entered already exists')
    new_word = crud.create_word(db,word)
    return new_word

@app.post("/new/wordlist",response_model=schemas.WordListOut)
def addwordlist(token: Annotated[str, Depends(oauth2_scheme)],wordlist: schemas.WordListBase,db:Session=Depends(get_db)):
    # needs protection
    wordlist_check = crud.get_wordlist(db,wordlist.word)
    if wordlist_check:
        raise HTTPException(status_code=400,detail='The word entered already exists')
    new_wordlist = crud.create_wordlist(db,wordlist)
    return new_wordlist

@app.post("/new/wordpic",response_model=schemas.WordPicOut)
def wordpic(wordpic:schemas.WordPictureBase,db:Session=Depends(get_db)):
    check_wordpic = crud.getwordpic(db,wordpic.wordlist_id)
    if check_wordpic:
        raise HTTPException(status_code=400,detail='The word already has a picture')
    newwordpic = crud.create_wordpic(db,wordpic)
    return newwordpic


@app.post("/uploadfile/{word_id}")
async def create_wordlist_pic(file: UploadFile,request: Request,word_id:int,db:Session=Depends(get_db)):
    wordlist_check = crud.getwordid(db,word_id)
    orig_file = file.file
    if not wordlist_check:    
        with Image(file=orig_file) as img:
            user = db.query(models.WordList).get(word_id)
            jpeg_bin = img.make_blob() # convert to binary string
            decoded_blob = base64.b64encode(jpeg_bin)
            with store_context(store):
                user.picture.from_blob(jpeg_bin)
                db.commit()
                db.refresh(user)
                return {"filename": user.picture.locate()}
    else:
        raise HTTPException(status_code=400,detail='The word already has a picture')

@app.put("/changepic/{word_id}")
async def create_wordlist_pic(file: UploadFile,request: Request,word_id:int,db:Session=Depends(get_db)):
    wordlist_check = crud.getwordid(db,word_id)
    orig_file = file.file
    with Image(file=orig_file) as img:
        user = db.query(models.WordList).get(word_id)
        jpeg_bin = img.make_blob() # convert to binary string
        decoded_blob = base64.b64encode(jpeg_bin)
        with store_context(store):
            user.picture.from_blob(jpeg_bin)
            db.commit()
            db.refresh(user)
            return {"filename": user.picture.locate()}

@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(get_db)) -> Token:
    # the username should be used as our email for now
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400,detail='There is no such user')
    status = crud.verify_password(form_data.password,user.hashed_password.encode('utf-8'))
    if not status:
        raise HTTPException(status_code=400,detail='Incorrect credentials')
    if status:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = crud.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type="bearer")

@app.get("/languages")
async def fetch_languages(db:Session=Depends(get_db)):
    languages = crud.fetch_languages(db)
    print(languages)
    return languages

@app.get("/language-families")
async def fetch_language_families(db:Session=Depends(get_db)):
    language_families = crud.fetch_language_families(db)
    print(language_families)
    return language_families


@app.get("/wordlist")
async def fetch_wordlist(db:Session=Depends(get_db)):
    words = crud.fetch_wordlist(db)
    return words
