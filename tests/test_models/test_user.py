#!/usr/bin/python3
"""
A unittest for User class
"""

import unittest
from models.user import User
from models.base_model import BaseModel
from models import storage
from datetime import datetime
import os
import time


class TestUserClass(unittest.TestCase):
    """Unittest class for testing class User
    Test the following attributes
    - email = ""
    - password = ""
    - first_name = ""
    - last_name = ""
"""
    def setUp(self):
        """setUp method"""
        self.u1 = User()
        self.u2 = User()
        # dict_storage = storage.all()
        # dict_storage = {}

    def tearDown(self):
        """tearDown method"""
        del self.u1
        del self.u2
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_User_id(self):
        """Test User instance id"""
        self.assertNotEqual(self.u1.id, self.u2.id)

    # ***************************************************************
    def test_User_email(self):
        """Test User email"""
        self.assertIsInstance(self.u1.email, str)
        self.u1.email = "radouane@alx.com"
        self.assertEqual(self.u1.email, "radouane@alx.com")

    def test_User_password(self):
        """Test User password"""
        self.assertIsInstance(self.u1.password, str)
        self.u1.password = "Mohammed"
        self.assertEqual(self.u1.password, "Mohammed")

    def test_User_firstname(self):
        """Test User firstname"""
        self.assertIsInstance(self.u1.first_name, str)
        self.u1.first_name = "Gabriel"
        self.assertEqual(self.u1.first_name, "Gabriel")

    def test_User_lastname(self):
        """Test User lastname"""
        self.assertIsInstance(self.u1.last_name, str)
        self.u1.last_name = "Seth"
        self.assertEqual(self.u1.last_name, "Seth")

    # *********************************************************
    def test_datetime_attr(self):
        """Test datetime attributes"""
        self.assertIsInstance(self.u1.created_at, datetime)
        self.assertIsInstance(self.u1.updated_at, datetime)

    def test_initial_values(self):
        """Test initial values for User class attributes"""
        self.assertEqual(self.u1.email, "")
        self.assertEqual(self.u1.password, "")
        self.assertEqual(self.u1.first_name, "")
        self.assertEqual(self.u1.last_name, "")

    def test_user_inherits_BaseModel(self):
        """Test if User inherits from BaseModel"""
        self.assertIsInstance(self.u1, BaseModel)

    def test_user_type(self):
        """Test if User instance is of the same type"""
        self.assertEqual(type(self.u1), User)

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
        instance = User(**dict_u1)
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
