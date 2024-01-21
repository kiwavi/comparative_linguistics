from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from Utils import crud, models, schemas
from . import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
