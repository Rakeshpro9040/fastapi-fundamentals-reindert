from datetime import datetime
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def welcome(name):
    """Return a friendly welcome message!"""
    return {"message": f"Welcome {name}, to the car sharing service!"}


@app.get("/date")
def date():
    """Return the current date/time!"""
    return {"message": datetime.now()}