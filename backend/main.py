from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user_router
import model
from database import engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
  'http://localhost:5173',

]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_headers=['*'],
  allow_methods=['*'],

)

app.include_router(user_router, prefix='/api') # brings the user endpoint to the main.py file/ fastapi application