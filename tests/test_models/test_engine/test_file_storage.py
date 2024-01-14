#!/usr/bin/python3
"""
A unittest for FileStorage class
"""

import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
import os


class TestFileStorage(unittest.TestCase):
    """ unittest for the FileStorage class """

    def setUp(self):
        """ the setup method, it executed before all the tests """
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)
        storage._FileStorage__objects = {}

    def test_save_and_reload(self):
        """ tests the save and reload methods of the FileStorage """
        obj = BaseModel()
        storage.new(obj)
        obj.name = "Mohamed"
        obj.newid = 55221
        storage.save()
        storage.reload()
        reloaded_object_key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertTrue(reloaded_object_key in
                        storage._FileStorage__objects)
        re_obj = storage._FileStorage__objects[reloaded_object_key]
        self.assertEqual(re_obj.newid, 55221)
        self.assertEqual(re_obj.name, "Mohamed")

    def test_save_empty_file(self):
        """ tests an empty file """
        storage.save()
        storage.reload()
        self.assertEqual(len(storage._FileStorage__objects), 0)

        # test the attributes (file_path, objects) -----------------------
    def test_file_path_initial(self):
        """ tests the initiale value/type of the file_path attr """
        file_path = storage._FileStorage__file_path
        self.assertEqual(file_path[-5:], ".json")
        self.assertEqual(file_path, "file.json")
        self.assertEqual(type(file_path), str)

    def test_objects_initial(self):
        """ tests the initiale value/type of the objects attr """
        objects = storage._FileStorage__objects
        self.assertEqual(objects, {})
        self.assertEqual(type(objects), dict)

    def test_objects_add_val(self):
        """ tests the initiale and the echo on it when we add another val """
        objects = storage._FileStorage__objects
        self.assertEqual(objects, {})
        model = BaseModel()
        key = "BaseModel." + model.id
        self.assertIn(key, objects)
        self.assertEqual(model, objects[key])

    # testing the methods all(self), , new(obj), save(self), reload(self) --
    def test_method_all_pass(self):
        """ tests the method `all` """
        self.assertEqual(storage.all(), {})
        self.assertEqual(type(storage.all()), dict)
        model = BaseModel()
        key = "BaseModel." + model.id
        self.assertIn(key, storage.all())
        self.assertEqual(model, storage.all()[key])

        model2 = BaseModel()
        key2 = "BaseModel." + model2.id
        self.assertNotEqual(model.id, model2.id)
        self.assertNotEqual(key, key2)

    def test_method_all_fail(self):
        """ tests the method `all` """
        with self.assertRaises(TypeError):
            storage.all(None)

    def test_method_new_pass(self):
        """ tests the method `new` """
        obj = {'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
               'created_at': '2017-09-28T21:03:54.052298',
               '__class__': 'BaseModel', 'my_number': 89,
               'updated_at': '2017-09-28T21:03:54.052302',
               'name': 'My_First_Model'}

        obj2 = {'id': 'wed431ef-ceff-efe5-98e5-e1f7f8q27fw7',
                'created_at': '2021-09-28T21:03:54.052298',
                '__class__': 'BaseModel', 'my_number': 89,
                'updated_at': '2021-09-28T21:03:54.052302',
                'name': 'My_Second_Model'}

        model = BaseModel(**obj)
        model2 = BaseModel(**obj2)

        objects = storage.all()

        key = "BaseModel." + model.id
        key2 = "BaseModel." + model2.id

        self.assertEqual(objects, {})
        storage.new(model)
        storage.new(model2)
        self.assertIn(key, objects.keys())
        self.assertIn(key2, objects.keys())

    def test_method_new_fail(self):
        """ tests the method `new` """
        with self.assertRaises(TypeError):
            storage.new(None, None)

        with self.assertRaises(AttributeError):
            storage.new(None)

    def test_method_save_pass(self):
        """ tests the method `save` """
        data = ""
        try:
            with open("file.json", "r", encoding="utf-8") as f:
                data = f.read()
        except Exception:
            pass

        model = BaseModel()
        objects = storage.all()

        self.assertNotEqual(objects, {})
        self.assertEqual(data, "")

        model.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = f.read()
        self.assertNotEqual(data, "")

    def test_method_save_fail(self):
        """ tests the method `save` """
        with self.assertRaises(TypeError):
            storage.save(None)

    def test_reload(self):
        """Tests reload deserializes JSON file to objects"""

        model = BaseModel()
        storage.new(model)
        key = "BaseModel." + model.id

        storage.save()
        storage.reload()
        objects = storage.all()
        self.assertIn(key, objects.keys())
        self.assertNotEqual(model, objects[key])

    def test_reload_args(self):
        """Tests reload args"""
        with self.assertRaises(TypeError):
            storage.reload("")
            storage.reload(None)
            storage.reload(int)

    def test_reload_file_missing(self):
        """Tests reload when file is missing"""
        try:
            os.remove("file.json")
        except (FileNotFoundError):
            pass

        try:
            storage.reload()
        except Exception as e:
            self.fail()


if __name__ == '__main__':
    unittest.main()
