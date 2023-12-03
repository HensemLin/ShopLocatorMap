import logging
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import db_models
from .database.db_setup import engine
from .database.db_init_values import initialize_table_data
from .Routers import *

db_models.Base.metadata.create_all(bind=engine)

initialize_table_data()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shop_router)
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": f"Welcome to my api"}