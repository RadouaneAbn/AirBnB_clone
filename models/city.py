#!/usr/bin/python3
# conatins the `City` class
###########################
from models.base_model import BaseModel


class City(BaseModel):
    """ The City Class """

    state_id = ""  # State.id
    name = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
