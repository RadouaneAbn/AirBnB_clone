#!/usr/bin/python3
# contains the `User` class
###########################
from models.base_model import BaseModel


class User(BaseModel):
    """ The User class which will contain the users's data """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    pass
