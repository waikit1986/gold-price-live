from fastapi import FastAPI

from db.database import Base, engine
from currencies import models_currencies
from user import models_user
from indicators import models_features
from yf import models_external_symbols
from ai import models_ai
from news import models_news
from user.router_user import router as user_router
from apple.router_apple import router as apple_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Gold Price Live API!"}

app.include_router(user_router, prefix="/api")
app.include_router(apple_router, prefix="/api")

Base.metadata.create_all(bind=engine)