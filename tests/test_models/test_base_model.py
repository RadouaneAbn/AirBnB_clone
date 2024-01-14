#!/usr/bin/python3
"""This is the ``test_base_model`` module
It contains tests for the BaseModel class
"""


from datetime import datetime
from datetime import timedelta
from io import StringIO
from models.base_model import BaseModel
from unittest.mock import patch
import unittest


class TestBaseModel(unittest.TestCase):
    """Defines a class TestBaseModel to test BaseModel class"""

    def setUp(self):
        """Set up all instances that will be used in each test"""
        self.bm1 = BaseModel()
        self.bm2 = BaseModel()

#   -----test for public instance attributes-----
    def test_id(self):
        """Tests all edge cases for the instance id"""

        self.assertIsInstance(self.bm1, BaseModel)
        self.assertTrue(hasattr(self.bm1, "id"))
        self.assertNotEqual(self.bm1.id, self.bm2.id)
        self.assertIsInstance(self.bm1.id, str)

    def test_created_at(self):
        """Tests for all edges cases for the instance created_at"""

        now = datetime.now()
        seconds = timedelta(seconds=1)
        self.assertAlmostEqual(self.bm1.created_at, now, delta=seconds)
        self.assertAlmostEqual(self.bm2.created_at, now, delta=seconds)
        self.assertTrue(hasattr(self.bm1, "created_at"))
        self.assertTrue(hasattr(self.bm2, "created_at"))
        self.assertIsInstance(self.bm1.created_at, datetime)
        self.assertIsInstance(self.bm2.created_at, datetime)

    def test_updated_at(self):
        """Tests all edge cases for the instance updated_at"""

        now = datetime.now()
        seconds = timedelta(seconds=1)
        self.assertAlmostEqual(self.bm1.updated_at, now, delta=seconds)
        self.assertAlmostEqual(self.bm2.updated_at, now, delta=seconds)
        self.assertTrue(hasattr(self.bm1, "updated_at"))
        self.assertTrue(hasattr(self.bm2, "updated_at"))
        self.assertIsInstance(self.bm1.updated_at, datetime)
        self.assertIsInstance(self.bm2.updated_at, datetime)

#   ------test for public instance methods-------

    def test_init(self):
        """Test for object recreation with json representation"""

        origin = BaseModel()

        self.assertIs(type(origin), BaseModel)
        origin.name = "Omar"
        origin.number = 89
        origin_dict = origin.to_dict()
        copy = BaseModel(**origin_dict)
        self.assertIs(type(copy), BaseModel)
        self.assertIsNot(origin, copy)
        class_map = {
                     "id": str,
                     "created_at": datetime,
                     "updated_at": datetime,
                     "name": str,
                     "number": int}
        for key, value in class_map.items():
            with self.subTest(key=key, value=value):
                self.assertIn(key, origin.__dict__)
                self.assertIn(key, copy.__dict__)
                self.assertIs(type(origin.__dict__[key]), value)
                self.assertIs(type(copy.__dict__[key]), value)
        self.assertEqual(origin.name, "Omar")
        self.assertEqual(copy.name, "Omar")
        self.assertEqual(origin.number, 89)
        self.assertEqual(copy.number, 89)

    def test_save(self):
        """Tests all edge cases for the save method"""

        now = datetime.now()
        seconds = timedelta(seconds=1)
        bm1_initial_updated_at = self.bm1.updated_at
        bm2_initial_updated_at = self.bm2.updated_at

        self.bm1.save()
        self.bm2.save()

        self.assertNotEqual(self.bm1.updated_at, bm1_initial_updated_at)
        self.assertNotEqual(self.bm2.updated_at, bm2_initial_updated_at)
        self.assertAlmostEqual(self.bm1.updated_at, now, delta=seconds)
        self.assertAlmostEqual(self.bm2.updated_at, now, delta=seconds)

    def test_to_dict(self):
        """Tests all edge cases for the return value of to_dict method"""

        self.bm1.name = "My first base model"
        self.bm1.number = 89
        updated_at = self.bm1.updated_at.isoformat()
        created_at = self.bm1.created_at.isoformat()

        expected = {"name": "My first base model", "number": 89,
                    "__class__": "BaseModel", "created_at": created_at,
                    "updated_at": updated_at, "id": self.bm1.id}

        self.assertDictEqual(self.bm1.to_dict(), expected)

        self.bm2.name = "My second base model"
        self.bm2.number = 53
        updated_at = self.bm2.updated_at.isoformat()
        created_at = self.bm2.created_at.isoformat()

        expected = {"name": "My second base model", "number": 53,
                    "__class__": "BaseModel", "created_at": created_at,
                    "updated_at": updated_at, "id": self.bm2.id}

        self.assertDictEqual(self.bm2.to_dict(), expected)

    def test_str(self):
        """Tests for edge cases for print value of __str__ method"""

        self.maxDiff = None

        class_name = self.bm1.__class__.__name__
        id = self.bm1.id
        bm1_dict = self.bm1.__dict__

        expected = "[{}] ({}) {}".format(class_name, id, bm1_dict)

        self.assertEqual(str(self.bm1), expected)

        with patch("sys.stdout", new=StringIO()) as str_out:
            print(self.bm1, end="")
            self.assertEqual(str_out.getvalue(), expected)
