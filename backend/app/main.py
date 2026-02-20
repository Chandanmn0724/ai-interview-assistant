from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import interview
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

# ADD THIS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview.router)

@app.get("/")
def home():
    return {"message": "Backend working successfully"}
