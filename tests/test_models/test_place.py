#!/usr/bin/python3
"""
A unittest for Place class
"""

import unittest
from models.place import Place
from models.base_model import BaseModel
from models import storage
from datetime import datetime
import os
import time


class TestPlaceClass(unittest.TestCase):
    """Unittest class for testing class Place
    Test the following attributes
    - name = ""
    """
    def setUp(self):
        """setUp method"""
        self.u1 = Place()
        self.u2 = Place()
        # dict_storage = storage.all()
        # dict_storage = {}

    def tearDown(self):
        """tearDown method"""
        del self.u1
        del self.u2
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_Place_id(self):
        """Test Place instance id"""
        self.assertNotEqual(self.u1.id, self.u2.id)

    # ***************************************************************
    def test_Place_name(self):
        """Test Place name"""
        self.assertIsInstance(self.u1.name, str)
        self.u1.name = "Mohamed"
        self.assertEqual(self.u1.name, "Mohamed")

    def test_Place_city_id(self):
        """Test Place city_id"""
        self.assertIsInstance(self.u1.city_id, str)
        self.u1.city_id = "id"
        self.assertEqual(self.u1.city_id, "id")

    def test_Place_user_id(self):
        """Test Place user_id"""
        self.assertIsInstance(self.u1.user_id, str)
        self.u1.user_id = "Mohamed"
        self.assertEqual(self.u1.user_id, "Mohamed")

    def test_Place_description(self):
        """Test Place description"""
        self.assertIsInstance(self.u1.description, str)
        self.u1.description = "Mohamed"
        self.assertEqual(self.u1.description, "Mohamed")

    def test_Place_number_rooms(self):
        """Test Place number_rooms"""
        self.assertIsInstance(self.u1.number_rooms, int)
        self.u1.number_rooms = 5
        self.assertEqual(self.u1.number_rooms, 5)

    def test_Place_number_bathrooms(self):
        """Test Place number_bathrooms"""
        self.assertIsInstance(self.u1.number_bathrooms, int)
        self.u1.number_bathrooms = 1
        self.assertEqual(self.u1.number_bathrooms, 1)

    def test_Place_max_guest(self):
        """Test Place max_guest"""
        self.assertIsInstance(self.u1.max_guest, int)
        self.u1.max_guest = 2
        self.assertEqual(self.u1.max_guest, 2)

    def test_Place_price_by_night(self):
        """Test Place price_by_night"""
        self.assertIsInstance(self.u1.price_by_night, int)
        self.u1.price_by_night = 15
        self.assertEqual(self.u1.price_by_night, 15)

    def test_Place_latitude(self):
        """Test Place latitude"""
        self.assertIsInstance(self.u1.latitude, float)
        self.u1.latitude = 5.5
        self.assertEqual(self.u1.latitude, 5.5)

    def test_Place_longitude(self):
        """Test Place longitude"""
        self.assertIsInstance(self.u1.longitude, float)
        self.u1.longitude = 5.5
        self.assertEqual(self.u1.longitude, 5.5)

    def test_Place_amenity_ids(self):
        """Test Place amenity_ids"""
        self.assertIsInstance(self.u1.amenity_ids, list)
        self.u1.amenity_ids = ["hi", "hi2"]
        self.assertEqual(self.u1.amenity_ids, ["hi", "hi2"])

    # *********************************************************
    def test_datetime_attr(self):
        """Test datetime attributes"""
        self.assertIsInstance(self.u1.created_at, datetime)
        self.assertIsInstance(self.u1.updated_at, datetime)

    def test_initial_values(self):
        """Test initial values for Place class attributes"""
        self.assertEqual(self.u1.name, "")
        self.assertEqual(self.u1.city_id, "")
        self.assertEqual(self.u1.user_id, "")
        self.assertEqual(self.u1.description, "")
        self.assertEqual(self.u1.number_rooms, 0)
        self.assertEqual(self.u1.number_bathrooms, 0)
        self.assertEqual(self.u1.max_guest, 0)
        self.assertEqual(self.u1.price_by_night, 0)
        self.assertEqual(self.u1.latitude, 0.0)
        self.assertEqual(self.u1.longitude, 0.0)
        self.assertEqual(self.u1.amenity_ids, [])

    def test_place_inherits_BaseModel(self):
        """Test if Place inherits from BaseModel"""
        self.assertIsInstance(self.u1, BaseModel)

    def test_place_type(self):
        """Test if Place instance is of the same type"""
        self.assertEqual(type(self.u1), Place)

    def test_storage_contains_instances(self):
        """Test storage contains the instances"""
        search_key = f"{self.u1.__class__.__name__}.{self.u1.id}"
        self.assertTrue(search_key in storage.all().keys())
        search_key = f"{self.u2.__class__.__name__}.{self.u2.id}"
        self.assertTrue(search_key in storage.all().keys())
        # self.u1.save()
        # self.u2.save()

    def test_to_dict_id(self):
        """Test to_dict method from BaseModel"""
        dict_u1 = self.u1.to_dict()
        self.assertIsInstance(dict_u1, dict)
        self.assertIn('id', dict_u1.keys())

    def test_to_dict_created_at(self):
        """Test to_dict method from BaseModel"""
        dict_u1 = self.u1.to_dict()
        self.assertIsInstance(dict_u1, dict)
        self.assertIn('created_at', dict_u1.keys())

    def test_to_dict_updated_at(self):
        """Test to_dict method from BaseModel"""
        dict_u1 = self.u1.to_dict()
        self.assertIsInstance(dict_u1, dict)
        self.assertIn('updated_at', dict_u1.keys())

    def test_to_dict_class_name(self):
        """Test to_dict method from BaseModel"""
        dict_u1 = self.u1.to_dict()
        self.assertEqual(self.u1.__class__.__name__, dict_u1["__class__"])

    def test_str_(self):
        """Test __str__ method from BaseModel"""
        cls_rp = str(self.u1)
        format = "[{}] ({}) {}".format(self.u1.__class__.__name__,
                                       self.u1.id, self.u1.__dict__)
        self.assertEqual(format, cls_rp)

    def test_check_two_instances_with_dict(self):
        """Test to check an instance created from a dict is different from
another"""
        dict_u1 = self.u1.to_dict()
        instance = Place(**dict_u1)
        self.assertIsNot(self.u1, instance)
        self.assertEqual(str(self.u1), str(instance))
        self.assertFalse(instance is self.u1)

    def test_save(self):
        """Test save() method from BaseModel"""
        update_old = self.u1.updated_at
        time.sleep(0.1)
        self.u1.save()
        updated_new = self.u1.updated_at
        self.assertNotEqual(update_old, updated_new)
