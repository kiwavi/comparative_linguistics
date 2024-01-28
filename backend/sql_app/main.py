from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from Utils import crud, models, schemas
from Utils.database import SessionLocal, engine
import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    db_user_check = crud.get_user_by_email(db, user.email)
    if db_user_check:
        raise HTTPException(status_code=400,detail='Email already exists')
    db_user = crud.create_user(db,user);
    return db_user

@app.post("/new/language-family",response_model=schemas.LanguageFamilyOut)
def addlanguagefamily(family:schemas.LanguageFamilyCreate,db:Session=Depends(get_db)):
    language_family_check = crud.get_language_family(db, family.name)
    if language_family_check:
        raise HTTPException(status_code=400,detail='Language family exists')
    new_language_family = crud.create_language_family(db,family)
    return new_language_family

@app.post("/new/language",response_model=schemas.LanguagesOut)
def addlanguage(language:schemas.LanguageCreate,db:Session=Depends(get_db)):
    language_check = crud.get_language(db,language.name)
    if language_check:
        raise HTTPException(status_code=400,detail='Language exists')
    new_language = crud.create_language(db,language)
    return new_language
