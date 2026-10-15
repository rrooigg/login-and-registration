# this file handles user-related endpoints i.e registration & login

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import bcrypt
import uuid # used to create unique identifiers for db records, session IDs etc
from jose import jwt

import os
from dotenv import load_dotenv

from database import SessionLocal
from model import User

user_router = APIRouter() # allows to group related endpoints together

load_dotenv()
SECRET_KEY= os.getenv("SECRET_KEY") # applied to the token to pprove it wasn't tempered with/ check for authenticity
ALGORITHM= 'HS256' # cryptographic algorithm to sign & verify JWT tokens 


class RegisterRequest(BaseModel):
  name: str
  email: str
  password: str
  user_type: str

class LoginRequest(BaseModel):
  email: str
  password: str

# use post reuest because data is hidden inside the request body but in get the data is sent to the url thus not used
@user_router.post('/register')
def register_user(user: RegisterRequest):
  db= SessionLocal()
  try:
    existing_user= db.query(User).filter(User.email == user.email).first()

    if existing_user:
      raise HTTPException(status_code=400, detail='User already exists')

    hashed_password= bcrypt.hashpw(
      user.password.encode('utf-8'),
      bcrypt.gensalt()
    ).decode('utf-8')

    user_id= str(uuid.uuid4())

    token= jwt.encode(
      {'user_id': user_id},
      SECRET_KEY,
      algorithm=ALGORITHM

    )

    new_user= User(
      user_id=user_id,
      name=user.name,
      email=user.email,
      password=hashed_password,
      user_type=user.user_type,
      token=token

    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
      'token':token,
      'user_id':user_id,
      'user_type':user.user_type

    }
  
  except Exception:
    db.rollback()
    raise
    
  finally:
    db.close()

@user_router.post('/login')
def login_user(user: LoginRequest):
  db= SessionLocal()
  try:
    found_user= db.query(User).filter(User.email == user.email).first()

    if not found_user or not bcrypt.checkpw(
      user.password.encode('utf-8'),
      found_user.password.encode('utf-8')
    ):
      raise HTTPException(
        status_code=400, detail='Invalid credentials'
      )
    token= jwt.encode(
      {'user_id': found_user.user_id},
      SECRET_KEY,
      algorithm=ALGORITHM

    )

    return {
      'token':token,
      'user_id':found_user.user_id,
      'user_type': found_user.user_type
    }

  finally:
    db.close()