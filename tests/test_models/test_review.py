#!/usr/bin/python3
"""
A unittest for Review class
"""

import unittest
from models.review import Review
from models.base_model import BaseModel
from models import storage
from datetime import datetime
import os
import time


class TestReviewClass(unittest.TestCase):
    """Unittest class for testing class Review
    Test the following attributes
    - name = ""
    """
    def setUp(self):
        """setUp method"""
        self.u1 = Review()
        self.u2 = Review()
        # dict_storage = storage.all()
        # dict_storage = {}

    def tearDown(self):
        """tearDown method"""
        del self.u1
        del self.u2
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_Review_id(self):
        """Test Review instance id"""
        self.assertNotEqual(self.u1.id, self.u2.id)

    # ***************************************************************
    def test_Place_place_id(self):
        """Test Place place_id"""
        self.assertIsInstance(self.u1.place_id, str)
        self.u1.place_id = "id"
        self.assertEqual(self.u1.place_id, "id")

    def test_Place_user_id(self):
        """Test Place user_id"""
        self.assertIsInstance(self.u1.user_id, str)
        self.u1.user_id = "id"
        self.assertEqual(self.u1.user_id, "id")

    def test_Place_text(self):
        """Test Place text"""
        self.assertIsInstance(self.u1.text, str)
        self.u1.text = "text"
        self.assertEqual(self.u1.text, "text")

    # *********************************************************
    def test_datetime_attr(self):
        """Test datetime attributes"""
        self.assertIsInstance(self.u1.created_at, datetime)
        self.assertIsInstance(self.u1.updated_at, datetime)

    def test_initial_values(self):
        """Test initial values for Review class attributes"""
        self.assertEqual(self.u1.user_id, "")
        self.assertEqual(self.u1.place_id, "")
        self.assertEqual(self.u1.text, "")

    def test_review_inherits_BaseModel(self):
        """Test if Review inherits from BaseModel"""
        self.assertIsInstance(self.u1, BaseModel)

    def test_review_type(self):
        """Test if Review instance is of the same type"""
        self.assertEqual(type(self.u1), Review)

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
        instance = Review(**dict_u1)
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
