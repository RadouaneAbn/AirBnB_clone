#!/usr/bin/env python3
# contains the FileStorage class
####################
import json
import os

class FileStorage:
    """ serializes instances to a JSON file and deserializes
    JSON file to instances """
    __file_path = "file.json"
    __objects = {}

    # @property
    def all(self):
        """ getter for the `__objects` private attribute """
        return self.__objects

    # @objects.setter
    def new(self, obj):
        """ setter for the `__objects` private attribute """
        self.__objects.update({f"{obj.__class__.__name__}.{obj.id}": obj})

    # @property
    def save(self):
        """ getter for the `__files_path` private attribute """
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            out = {}
            for key, value in self.__objects.items():
                out[key] = value.to_dict()
            f.write(json.dumps(out))

    # @objects.setter
    def reload(self):
        """ setter for the `__file_path` private attribute """
        from ..user import User
        from ..base_model import BaseModel
        available = ['User', 'BaseMode']
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                data = f.read()
            if data.strip():
                data = json.loads(data)
                for key, value in data.items():
                    print(key)  # GDB
                    key_val = key.split(".")[0]
                    if key_val == available[0]:
                        self.__objects[key] = User(**value)
                    elif key_val == available[1]:
                        self.__objects[key] = BaseModel(**value)
                # self.__objects.update(json.loads(data))
