import uvicorn
from fastapi import FastAPI, HTTPException
from sqlmodel import create_engine, SQLModel, Session

from schemas import load_db, save_db, CarInput, CarOutput, TripOutput, TripInput, Car

app = FastAPI(title="fastapi-fundamentals-reindert-openapi")

db = load_db()
# Replaced dict with object so access like car.id instead of car["id"]


engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},  # Needed for SQLite, to run threads in async way
    echo=True  # Log generated SQL, in prod set this as off
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    # Here it will create db and model class object as table


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
@app.post(path="/api/cars/", response_model=Car)
def add_car(car_input: CarInput) -> Car:
    with Session(engine) as session:
        new_car = Car.from_orm(car_input)
        session.add(new_car)
        session.commit()
        session.refresh(new_car)
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


# Here car_id is query parameter and trip as request body
@app.post(path="/api/cars/{car_id}/trips", response_model=TripOutput)
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
    matches = [car for car in db if car.id == car_id]
    if matches:
        car = matches[0]
        new_trip = TripOutput(id=len(car.trips)+1,
                              start=trip.start, end=trip.end,
                              description=trip.description)
        car.trips.append(new_trip)
        save_db(db)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}")


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)