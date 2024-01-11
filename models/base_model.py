#!/usr/bin/env python3
# contains the class BaseModel that defines all common attributes/methods
# for other classes.
####################
import uuid
from datetime import datetime
from . import storage

class BaseModel:
    """ defines all common attributes/methods for other classes. """

    def __init__(self, *args, **kwargs):
        """ the initialization of any new instance """
        if kwargs:
            self.__dict__.update({k: v for k, v in kwargs.items()
                                  if k != "__class__"})
            self.__dict__["created_at"] = datetime.fromisoformat(
                self.__dict__["created_at"])
            self.__dict__["updated_at"] = datetime.fromisoformat(
                self.__dict__["updated_at"])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """ the string to represintation of the instance """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
    # self now is refering to whatever class is calling this method

    def save(self):
        """ updates the public instance attribute `updated_at` """
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """ returns a dictionary containing all keys/values of __dict__
        of the instance """
        out = self.__dict__.copy()     # self.__dict__ affects the source
        out['__class__'] = self.__class__.__name__
        out['created_at'] = out['created_at'].isoformat()
        out['updated_at'] = out['updated_at'].isoformat()

        return out
    pass
