#!/usr/bin/python3
# contains the Review class
############################
from models.base_model import BaseModel


class Review(BaseModel):
    """ the review class which contains the reviews """
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, **kwargs):
        """ initialization for each new instance """
        super().__init__(**kwargs)
    pass
