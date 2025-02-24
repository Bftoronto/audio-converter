from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    token = Column(String, unique=True)

class AudioRecord(Base):
    __tablename__ = "audio_records"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    file_path = Column(String)
    format = Column(String) 