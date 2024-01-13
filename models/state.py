#!/usr/bin/python3
# contains the `State` class
############################
from models.base_model import BaseModel


class State(BaseModel):
    """ The State class """
    name = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
