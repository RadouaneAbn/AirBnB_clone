#!/usr/bin/python3
"""This is the ``test_file_storage`` module
It defines all tests for the class FileStorage
"""

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import json
import os
import unittest


class TestFileStorage(unittest.TestCase):
    """Defines a class TestFileStorage that defines tests
    for class FileStorage
    """

    def setUp(self):
        """Sets up all intances needed for the test methods"""
        self.bm = BaseModel()
        self.storage = FileStorage()

    def tearDown(self):
        """Clean up test file"""
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_initialization_without_args(self):
        """Tests for class FileStorage initialization without args"""
        with self.assertRaises(TypeError):
            FileStorage(None)
            FileStorage("Test")

# -------------tests for class attributes----------------------
    def test_file_path(self):
        """Tets for the type of the class attribute file_path"""

        file_path = FileStorage._FileStorage__file_path
        self.assertEqual(type(file_path), str)
        self.assertFalse(hasattr(self.storage, '__file_path'))
        self.assertEqual(file_path, "file.json")

    def test_objects(self):
        """Tets for class attribute objects"""

        objects = FileStorage._FileStorage__objects
        result = self.storage.all()
        self.assertEqual(type(objects), dict)
        self.assertFalse(hasattr(self.storage, '__objects'))
        self.assertEqual(result, objects)

    def test_objects_empty(self):
        """Tests the objects attribute is empty
        immediately after instance is created
        """
        storage = FileStorage()
        objects = FileStorage._FileStorage__objects

# ---------tests for public intance methods----------------
    def test_all(self):
        """Defines all test cases for the intance method all()"""
        objects = FileStorage._FileStorage__objects
        result = self.storage.all()
        self.assertEqual(type(result), dict)
        self.assertEqual(result, objects)

    def test_all_returns_empty_dict(self):
        """Tests all returns empty dictionary"""
        FileStorage._FileStorage__objects = {}
        result = self.storage.all()
        self.assertEqual(result, {})

    def test_all_args(self):
        """Defines tests for all with args"""
        with self.assertRaises(TypeError):
            self.storage.all("test")
            self.storage.all("test", "test")
            self.storage.all(None)

    def test_new(self):
        """Tests new adds object to the objects attribute"""

        self.storage.new(self.bm)
        objects = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + self.bm.id, objects.keys())
        self.assertIn(self.bm, objects.values())

    def test_new_arg(self):
        """Tests new raises type error with wrong args"""
        with self.assertRaises(TypeError):
            self.storage.new()

    def test_new_invalid_args(self):
        """Tests for invalid args used with new method of class FileStorage"""
        with self.assertRaises(AttributeError):
            self.storage.new("")
            self.storage.new(None, None)

    def test_save(self):
        """Defines all edge case tests for the method save()"""

        self.storage.new(self.bm)

        self.storage.save()
        bm_key = "BaseModel." + self.bm.id

        with open("file.json", "r") as f:
            data = json.load(f)
        self.assertIn(bm_key, data.keys())

    def test_save_args(self):
        """Tests whether save accepts arguments"""

        with self.assertRaises(TypeError):
            self.storage.save("Test")
            self.storage.save("Test", "Test")
            self.storage.save(None)

    def test_reload(self):
        """Tests reload deserializes JSON file to objects"""

        self.storage.new(self.bm)
        bm_key = "BaseModel." + self.bm.id

        self.storage.save()
        self.storage.reload()
        objects = FileStorage._FileStorage__objects
        self.assertIn(bm_key, objects.keys())
        self.assertNotEqual(self.bm, objects[bm_key])

    def test_reload_args(self):
        """Tests reload args"""
        with self.assertRaises(TypeError):
            self.storage.reload("")
            self.storage.reload(None)
            self.storage.reload(int)

    def test_reload_file_missing(self):
        """Tests reload when file is missing"""
        try:
            os.remove("file.json")
        except (FileNotFoundError):
            pass

        try:
            self.storage.reload()
        except Exception as e:
            self.fail()
