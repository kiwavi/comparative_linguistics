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
