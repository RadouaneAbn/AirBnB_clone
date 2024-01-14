#!/usr/bin/python3
# unittest for the the base class `BaseModel`
#############################
import unittest
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """ all the test cases for the `BaseModel` class """

    def setUp(self):
        """ setup for all the coming tests """
        self.base_model = BaseModel()

    def test_id_generation(self):
        """ tests the `id` instance attribute """
        self.assertIsNotNone(self.base_model.id)
        self.assertIsInstance(self.base_model.id, str)

    def test_created_at(self):
        """ tests the `created_at` instance attribute """
        self.assertIsInstance(self.base_model.created_at, datetime)

    def test_updated_at(self):
        """ tests the `updated_at` instance attribute """
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_save_updates_updated_at(self):
        """ tests the `save` instance method """
        old_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertNotEqual(old_updated_at, self.base_model.updated_at)

    def test_to_dict(self):
        """ tests the `to_dict` instance method """
        model_dict = self.base_model.to_dict()
        created_at = self.base_model.created_at.isoformat()
        updated_at = self.base_model.updated_at.isoformat()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIn('__class__', model_dict)
        self.assertEqual(model_dict['id'], self.base_model.id)
        self.assertEqual(model_dict['created_at'], created_at)
        self.assertEqual(model_dict['updated_at'], updated_at)
        self.assertEqual(model_dict['__class__'], 'BaseModel')

    def test_kwargs(self):
        model_dict = self.base_model.to_dict()
        model2 = BaseModel(**model_dict)
        self.assertEqual(model2.id, self.base_model.id)
        self.assertEqual(model2.created_at, self.base_model.created_at)
        self.assertEqual(model2.updated_at, self.base_model.updated_at)
        self.assertNotEqual(model2, self.base_model)

        model3 = BaseModel(232, 'hi', None)
        self.assertNotEqual(model2.id, 232)
        self.assertNotEqual(model2.created_at, 'hi')
        self.assertNotEqual(model2.updated_at, None)

        obj_values = {
                        'id': 'custom_id',
                        'created_at': '2022-01-01T12:00:00',
                        'updated_at': '2022-01-02T12:00:00'
        }
        base_model = BaseModel(**obj_values)
        self.assertEqual(base_model.id, 'custom_id')
        self.assertEqual(base_model.created_at,
                         datetime.fromisoformat('2022-01-01T12:00:00'))
        self.assertEqual(base_model.updated_at,
                         datetime.fromisoformat('2022-01-02T12:00:00'))

        partial_values = {
            'id': 'custom_id',
            'created_at': '2022-01-01T12:00:00',
        }
        base_model = BaseModel(**partial_values)
        self.assertNotEqual(base_model.id, 'custom_id')
        self.assertNotEqual(base_model.created_at,
                         datetime.fromisoformat('2022-01-01T12:00:00'))


if __name__ == '__main__':
    unittest.main()
