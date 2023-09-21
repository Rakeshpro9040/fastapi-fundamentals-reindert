import json
from pydantic import BaseModel


class Car(BaseModel):
    # This inherits BaseModel __init__ method
    id: int
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"


"""
Test this with below commands (Only kwargs allowed) -
from schemas import Car
c = Car(id=1, size="m", fuel="gas", doors=100, transmission="car")
c = Car(id=1, size="m", doors=100)
c.json()
c.dict()
"""


def load_db() -> list[Car]:
    """Load a list of Car objects from a JSON file"""
    with open("cars.json") as f:
        return [Car.parse_obj(obj) for obj in json.load(f)]


"""
parse_obj is a pydantic method, which takes dict and return that as obj
"""


def save_db(cars: list[Car]):
    with open("cars.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)

