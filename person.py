from pydantic import BaseModel, PositiveInt


class Person(BaseModel):
    name: str | None = None
    age: PositiveInt | None = None
