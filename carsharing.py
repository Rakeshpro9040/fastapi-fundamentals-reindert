from datetime import datetime
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def welcome():
    """Return a friendly welcome message!"""
    return {"message": "Welcome to the car sharing service!"}


@app.get("/date")
def welcome():
    """Return a friendly welcome message!"""
    return {"message": datetime.now()}