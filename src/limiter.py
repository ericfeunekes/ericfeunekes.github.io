import numpy as np
from pydantic import BaseModel, conint

class Limit(BaseModel):
    max_calls: conint(gt=0) #type:ignore
    period: conint(gt=0) = int(60e9) #type: ignore

    _times_released: list | None

    class Config:
        underscore_attrs_are_private = True
        allow_mutation = False

    def __init__(self, **data):
        super().__init__(**data)
    
    def acquire(self):
        pass
