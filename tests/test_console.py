#!/usr/bin/python3

import cmd
from io import StringIO
import re
import os
import uuid
import json
from unittest.mock import patch
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.place import Place
from models.state import State
from models import FileStorage
from models import storage
import unittest
import console


def check_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


# This args should be ignored
ignore = "this should be ignored"
classes = ['BaseModel', 'User', 'City', 'State',
           'Place', 'Amenity', 'Review']
wrong_classes = ['baseModel', 'user', 'city', 'state',
                 'place', 'amenity', 'review', 'ret']

dicts = {"BaseModel": '{"key": "value"}',
         "User": '{"full name": "alx SE", "Age": 25, "born": 1986}',
         "City": '{"name": "Safi", "best location": "sidi bouzid"}',
         "State": '{"name": "doukala"}',
         "Place": '{"name": "the kings mantion"}',
         "Amenity": '{"i have": "no idea what this is"}',
         "Review": '{"rate": 10}'}

dict_expected = {"BaseModel": ["'key': 'value'"],
                 "User": ["'full name': 'alx SE'",
                          "'Age': 25",
                          "'born': 1986"],
                 "City": ["'name': 'Safi'",
                          "'best location': 'sidi bouzid'"],
                 "State": ["'name': 'doukala'"],
                 "Place": ["'name': 'the kings mantion'"],
                 "Amenity": ["'i have': 'no idea what this is'"],
                 "Review": ["'rate': 10"]}

wrong_dict = {"BaseModel": '{"key": }',
              "User": '{"full name": "alx SE", "Age": 25, "born": 1986}',
              "City": '{"name": "Safi", "best location": "sidi bouzid"}',
              "State": '{"name": "doukala"}',
              "Place": '{"name": "the kings mantion"}',
              "Amenity": '{"i have": "no idea what this is"}',
              "Review": '{"rate": 10}'}

class_missing = "** class name missing **\n"
no_class = "** class doesn't exist **\n"
id_missing = "** instance id missing **\n"
no_inst = "** no instance found **\n"
no_attr_name = "** attribute name missing **\n"
no_attr_value = "** value missing **\n"
syn_msg = "*** Unknown syntax:"

json_file = storage._FileStorage__file_path
help_msg = """
Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

"""


class TestConsole(unittest.TestCase):
    """ Test cases for the console """

    @classmethod
    def setUp(self):
        try:
            os.rename(json_file, "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}
        storage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove(json_file)
        except IOError:
            pass
        try:
            os.rename("tmp", json_file)
        except IOError:
            pass

    def test_docstring(self):
        """Test docstrings exist in console.py"""
        self.assertTrue(len(console.__doc__) >= 1)

        """Test docstrings exist in test_console.py"""
        self.assertTrue(len(self.__doc__) >= 1)

    def test_prompt(self):
        """Test the prompt of teh console"""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_help(self):
        cmds = ['create', 'show', 'all', 'destroy'
                'update', 'quit', 'EOF']
        for cmd in cmds:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"help {cmd}")
                self.assertNotEqual(f.getvalue(), "")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            help = f.getvalue()
            self.assertEqual(help, help_msg)

    def test_emptyString(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual(f.getvalue(), "")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("          ")
            self.assertEqual(f.getvalue(), "")

    def test_non_existing_command(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("exist")
            self.assertEqual(f.getvalue(), "*** Unknown syntax: exist\n")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Create")
            self.assertEqual(f.getvalue(), "*** Unknown syntax: Create\n")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.all")
            self.assertEqual(f.getvalue(), "*** Unknown syntax: User.all\n")

    def test_create_success(self):
        ids = []
        inst = {}
        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                id_tmp = f.getvalue().strip('\n')
                ids.append(id_tmp)
                inst[class_name] = f"{class_name}.{id_tmp}"
                self.assertTrue(check_uuid(id_tmp))

            self.assertTrue(len(ids) == len(set(ids)))
            with open(json_file, "r") as file:
                data = json.loads(file.read())
            self.assertTrue(inst[class_name] in data)

    def test_create_error(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue(), class_missing)

        for class_name in wrong_classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                self.assertEqual(f.getvalue(), no_class)

    def test_show_success(self):
        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                id_tmp = f.getvalue().strip('\n')

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {class_name} {id_tmp}")
                data = f.getvalue().strip('\n')
                result = re.match(r'\[\S+\]\s?\((\S+)\)', data)
                self.assertEqual(result.group(1), id_tmp)

    def test_show_errors(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual(f.getvalue(), class_missing)

        for class_name in wrong_classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {class_name}")
                self.assertEqual(f.getvalue(), no_class)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {class_name}")
                self.assertEqual(f.getvalue(), id_missing)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"show {class_name} wrong_id this should be ignored")
                self.assertEqual(f.getvalue(), no_inst)

    def test_destroy_success(self):
        inst = {}
        for cl in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {cl}")
                id_tmp = f.getvalue().strip()
                inst[cl] = f"{cl}.{id_tmp}"

            with open(json_file, "r") as file:
                data = json.loads(file.read())
            self.assertTrue(inst[cl] in data)

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"destroy {cl} {id_tmp}")
                self.assertFalse(f"{cl}.{id_tmp}" in storage.all())

            with open(json_file, "r") as file:
                data = json.loads(file.read())
            self.assertFalse(inst[cl] in data)

    def test_destroy_errors(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            self.assertEqual(f.getvalue(), class_missing)

        for class_name in wrong_classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"destroy {class_name}")
                self.assertEqual(f.getvalue(), no_class)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"destroy {class_name}")
                self.assertEqual(f.getvalue(), id_missing)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"destroy {class_name} wrong_id this should be ignored")
                self.assertEqual(f.getvalue(), no_inst)

    def test_all_success(self):
        list_inst = []
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            self.assertEqual(f.getvalue(), "[]\n")

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {class_name}")
                self.assertEqual(f.getvalue(), "[]\n")

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {class_name} {ignore}")
                tmp_line = f.getvalue().strip('\n')
                list_inst.append(tmp_line)
                self.assertNotEqual(tmp_line, "")

    def test_all_error(self):
        for class_name in wrong_classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {class_name}")
                self.assertEqual(f.getvalue(), no_class)

    def test_update_success(self):
        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                tmp_id = f.getvalue().strip('\n')
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"update {class_name} {tmp_id} "
                                     f"\"key 15de\" \"test file\" {ignore}")
                HBNBCommand().onecmd(
                    f"show {class_name} {tmp_id}")
                data = f.getvalue()
                self.assertTrue("key 15de" in data)
                self.assertTrue("test file" in data)
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"update {class_name} {tmp_id} age 25 {ignore}")
                HBNBCommand().onecmd(f"show {class_name} {tmp_id}")
                data = f.getvalue()
                self.assertTrue("'age': 25" in data)

    def test_update_error(self):
        ids = {}
        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                ids[class_name] = f.getvalue().strip('\n')

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"update")
            self.assertEqual(f.getvalue(), class_missing)

        for class_name in wrong_classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"update {class_name}")
                self.assertEqual(f.getvalue(), no_class)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"update {class_name}")
                self.assertEqual(f.getvalue(), id_missing)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"update {class_name} wrong_id")
                self.assertEqual(f.getvalue(), no_inst)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"update {class_name} {ids[class_name]}")
                self.assertEqual(f.getvalue(), no_attr_name)
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"update {class_name} {ids[class_name]} key_15")
                self.assertEqual(f.getvalue(), no_attr_value)

    def test_default_success(self):
        ids = {}
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.all()")
            self.assertEqual(f.getvalue(), "[]\n")

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.create()")
                ids[class_name] = f.getvalue().strip('\n')

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"{class_name}.show(\"{ids[class_name]}\")")
                data = f.getvalue().strip('\n')
                result = re.match(r'\[\S+\]\s?\((\S+)\)', data)
                self.assertEqual(result.group(1), ids[class_name])

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"{class_name}.update(\"{ids[class_name]}\", "
                    f"\"full name\", \"alx SE\")")
                HBNBCommand().onecmd(
                    f"{class_name}.update(\"{ids[class_name]}\", Year, 2024)")
                HBNBCommand().onecmd(
                    f"{class_name}.show(\"{ids[class_name]}\")")
                data = f.getvalue()
                self.assertTrue("'full name': 'alx SE'" in data)
                self.assertTrue("'Year': 2024" in data)

        for i in range(10):
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"User.create()")

        for i in range(4):
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"City.create()")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"User.count()")
            self.assertEqual(f.getvalue().strip(), "11")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"BaseModel.count()")
            self.assertEqual(f.getvalue().strip(), "1")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"City.count()")
            self.assertEqual(f.getvalue().strip(), "5")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"class.count()")
            self.assertEqual(f.getvalue().strip(), "0")

    def test_default_dictionary(self):
        ids = {}
        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.create()")
                ids[class_name] = f.getvalue().strip('\n')

        for cl in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"{cl}.update(\"{ids[cl]}\", {dicts[cl]})")
                HBNBCommand().onecmd(f"{cl}.show({ids[cl]})")
                data = f.getvalue().strip()
                for string in dict_expected[cl]:
                    self.assertTrue(string in data)

    def test_default_errors(self):
        cmds = ['all', 'create', 'destroy', 'count', 'show', 'update']
        ucmds = ['mess', 'collect', 'try', 'ret', 'class']
        ids = {}

        # all the command shouldn't raise an exception
        for cmd in cmds:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"User.{cmd}")
                self.assertEqual(f.getvalue(), f"{syn_msg} User.{cmd}\n")
            with patch('sys.stdout', new=StringIO()) as f:
                try:
                    HBNBCommand().onecmd(f"User.{cmd}(None)")
                except Exception as e:
                    self.fail(e)

        # no existing class
        for class_name in wrong_classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.create()")
                self.assertEqual(f.getvalue(), no_class)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.show()")
                self.assertEqual(f.getvalue(), id_missing)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.show(wrong_uuid)")
                self.assertEqual(f.getvalue(), no_inst)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.create({ignore})")
                ids[class_name] = f.getvalue().strip('\n')

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.update()")
                self.assertEqual(f.getvalue(), id_missing)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"{class_name}.update(wrong_id)")
                self.assertEqual(f.getvalue(), no_inst)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"{class_name}.update(\"{ids[class_name]}\")")
                self.assertEqual(f.getvalue(), no_attr_name)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    f"{class_name}.update(\"{ids[class_name]}\", "
                    f"\"full name\")")
                self.assertEqual(f.getvalue(), no_attr_value)

        for cmd in ucmds:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"User.{cmd}()")
                self.assertEqual(f.getvalue(),
                                 f"{syn_msg} User.{cmd}()\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
