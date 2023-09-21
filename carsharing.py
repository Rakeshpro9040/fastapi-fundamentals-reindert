from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, save_db, CarInput, CarOutput

app = FastAPI(title="fastapi-fundamentals-reindert-openapi")

db = load_db()
# Replaced dict with object so access like car.id instead of car["id"]


@app.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None) -> list:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int):
    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        # HTTPException is the in-built fastAPI method to raise exception
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


# Here CarOutput is an argument to the decorator
# This will be used by the fastapi to validate the response of our functions
@app.post("/api/cars/", response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    # id=len(db)+1 will be later replaced by DB's sequence/identity column
    new_car = CarOutput(size=car.size, doors=car.doors,
                        fuel=car.fuel, transmission=car.transmission,
                        id=len(db)+1)
    db.append(new_car)
    save_db(db)
    return new_car


@app.delete(path="/api/cars/{id}", status_code=204)
def remove_car(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}")


@app.put(path="/api/cars/{id}", response_model=CarOutput)
def change_car(id: int, new_data: CarInput) -> CarOutput:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}")


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)