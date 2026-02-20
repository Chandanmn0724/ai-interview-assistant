from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class InterviewAttempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    difficulty = Column(String)
    score = Column(Integer)
    feedback = Column(Text)