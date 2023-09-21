import json
from pydantic import BaseModel


class TripInput(BaseModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


class CarInput(BaseModel):
    # This inherits BaseModel __init__ method
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

    # Instead the client tools generates dummy data
    # We can use the below to provide dummy data to fastapi
    class Config:
        json_schema_extra = {
            "example": {
                "size": "m",
                "doors": 4,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }


"""
Test this with below commands (Only kwargs allowed) -
from schemas import Car
c = Car(id=1, size="m", fuel="gas", doors=100, transmission="car")
c = Car(id=1, size="m", doors=100)
c.json()
c.dict()
"""


# from client we will not take id as input, but we must return it
class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []


def load_db() -> list[CarOutput]:
    """Load a list of Car objects from a JSON file"""
    with open("cars.json") as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]


"""
parse_obj is a pydantic method, which takes dict and return that as obj
"""


def save_db(cars: list[CarInput]):
    with open("cars.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)

