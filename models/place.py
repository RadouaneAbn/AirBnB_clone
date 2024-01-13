#!/usr/bin/python3
# contains the `Place` class
###########################
from models.base_model import BaseModel


class Place(BaseModel):
    city_id = ""  # City.id
    user_id = ""  # User.id
    name = ""
    description = ""
    number_rooms = int(0)
    number_bathrooms = int(0)
    max_guest = int(0)
    price_by_night = int(0)
    latitude = float(0.0)
    longitude = float(0.0)
    amenity_ids = []  # list of Amenity.id

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
