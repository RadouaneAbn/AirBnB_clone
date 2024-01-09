#!/usr/bin/python3

from datetime import datetime
import uuid


class BaseModel():

    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            self.__dict__.update(kwargs)
            self.__dict__['created_at'] = datetime.fromisoformat(self.__dict__['created_at'])
            self.__dict__['updated_at'] = datetime.fromisoformat(self.__dict__['updated_at'])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        return (f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        dict_inst = self.__dict__
        dict_inst['__class__'] = f'{self.__class__.__name__}'
        dict_inst['created_at'] = dict_inst['created_at'].isoformat()
        dict_inst['updated_at'] = dict_inst['updated_at'].isoformat()

        return (dict_inst)
