#!/usr/bin/python3
# contains the Amenity class
############################
from models.base_model import BaseModel


class Amenity(BaseModel):
    """ the amenity class which contains the amenity informations """
    name = ''

    def __init__(self, **kwargs):
        """ initialization for each new instance """
        super().__init__(**kwargs)
    pass
