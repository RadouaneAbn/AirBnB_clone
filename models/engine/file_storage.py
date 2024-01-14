#!/usr/bin/python3
"""
contains the FileStorage class, which will be the storage handler for
the whole project, it'll serialize/deserialize and handle the transformation
between data base (file for now).
"""

import json
import os


class FileStorage:
    """ serializes instances to a JSON file and deserializes
    JSON file to instances """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ getter for the `__objects` private attribute """
        return self.__objects

    def new(self, obj):
        """ setter for the `__objects` private attribute """
        self.__objects.update({f"{obj.__class__.__name__}.{obj.id}": obj})

    def save(self):
        """ getter for the `__files_path` private attribute """
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            out = {}
            for key, value in self.__objects.items():
                out[key] = value.to_dict()
            f.write(json.dumps(out))

    def reload(self):
        """ setter for the `__file_path` private attribute """
        from ..user import User
        from ..base_model import BaseModel
        from ..amenity import Amenity
        from ..review import Review
        from ..city import City
        from ..place import Place
        from ..state import State

        classes = {'User': User, 'BaseModel': BaseModel,
                   'Amenity': Amenity, 'Review': Review,
                   'City': City, 'Place': Place,
                   'State': State}

        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                data = f.read()
            if data.strip():
                data = json.loads(data)
                for key, value in data.items():  # key = mode.id
                    key_val = key.split(".")[0]
                    self.__objects[key] = classes[key_val](**value)
