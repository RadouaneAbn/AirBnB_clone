#!/usr/bin/python3

import cmd
from io import StringIO
import re
import os
import uuid
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

    def setUp(self):
        try:
            os.remove(json_file)
        except Exception:
            pass
        storage._FileStorage__objects = {}

    def test_help(self):
        cmds = ['create', 'show', 'all', 'destroy'
                'update', 'quit', 'EOF']
        for cmd in cmds:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("help {cmd}")
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
        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                id_tmp = f.getvalue().strip('\n')
                ids.append(id_tmp)
                self.assertTrue(check_uuid(id_tmp))

            self.assertTrue(len(ids) == len(set(ids)), "repeted uuid")

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
        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                id_tmp = f.getvalue().strip('\n')

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"destroy {class_name} {id_tmp}")
                self.assertFalse(f"{class_name}.{id_tmp}" in storage.all())

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
                id_tmp = f.getvalue().strip('\n')
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

    def test_default_errors(self):
        cmds = ['all', 'create', 'destroy', 'count', 'show', 'update']
        for cmd in cmds:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"User.{cmd}")
                self.assertEqual(f.getvalue(), f"{syn_msg} User.{cmd}\n")
            with patch('sys.stdout', new=StringIO()) as f:
                try:
                    HBNBCommand().onecmd(f"User.{cmd}(None)")
                except Exception as e:
                    self.fail(e)

        for class_name in wrong_classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.create()")
                self.assertEqual(f.getvalue(), no_class)

        for class_name in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.show()")
                self.assertEqual(f.getvalue(), id_missing)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
