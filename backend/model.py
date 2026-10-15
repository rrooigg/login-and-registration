from sqlalchemy import Column, String
from database import Base

class User(Base):
  __tablename__= 'users'

  user_id= Column(String, primary_key=True, index=True)
  name= Column(String, nullable=False)
  email= Column(String, unique=True, nullable=False, index=True)
  password= Column(String,nullable=False)
  user_type= Column(String, nullable=False)
  token= Column(String, nullable=True)