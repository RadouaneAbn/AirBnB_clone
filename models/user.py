#!/usr/bin/python3
"""
contains the `User` class which contains the user's data
email, password, firstname, last_name
"""
from models.base_model import BaseModel


class User(BaseModel):
    """ The User class which will contain the users's data
    like: email, password, firstname, lastname. and it
    inherates from the partent `BaseModel`."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    pass
