#!/usr/bin/python3
"""
A unittest for FileStorage class
"""

import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import os


class TestFileStorage(unittest.TestCase):
    """ unittest for the FileStorage class """

    def setUp(self):
        """ the setup method, it executed before all the tests """
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)
        FileStorage._FileStorage__objects = {}

    def test_save_and_reload(self):
        """ tests the save and reload methods of the FileStorage """
        obj = BaseModel()
        FileStorage().new(obj)
        obj.name = "Mohamed"
        obj.newid = 55221
        FileStorage().save()
        FileStorage().reload()
        reloaded_object_key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertTrue(reloaded_object_key in
                        FileStorage._FileStorage__objects)
        re_obj = FileStorage._FileStorage__objects[reloaded_object_key]
        self.assertEqual(re_obj.newid, 55221)
        self.assertEqual(re_obj.name, "Mohamed")

    def test_save_empty_file(self):
        """ tests an empty file """
        FileStorage().save()
        FileStorage().reload()
        self.assertEqual(len(FileStorage._FileStorage__objects), 0)


if __name__ == '__main__':
    unittest.main()
