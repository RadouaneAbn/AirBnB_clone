#!/usr/bin/env python3
# a program that contains the entry point of the command interpretter
######################
import cmd
import re
import shlex
from models.base_model import BaseModel
from models.user import User
from models import storage

class_missing = "** class name missing **"
class_nexist = "** class doesn't exist **"
id_missing = "** instance id missing **"
inst_missing = "** no instance found **"
attr_name_missing = "** attribute name missing **"
attr_value_missing = "** value missing **"


class HBNBCommand(cmd.Cmd):
    """ the console interpreter """
    prompt = "(hbnb) "

    def do_quit(self, line):
        """ quits the program """
        return True

    def do_EOF(self, line):
        """ exits the program """
        print()
        return True

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.
        If this method is not overridden, it repeats the last nonempty
        command entered."""
        pass

    def do_create(self, line):
        """ create <classname>
        Create a new instance from the <classname> """
        if line:
            class_name = line.split()[0]
            try:
                class_obj = globals()[class_name]
                new_obj = class_obj()
                new_obj.save()
                print(new_obj.id)
            except KeyError:
                print(class_nexist)
        else:
            print(class_missing)

    def do_show(self, line):
        """ show <classname> <id>
        print string representation of the instance """

        args = line.split()
        if len(args) == 0:
            print(class_missing)
            return

        try:
            class_obj = globals()[args[0]]
        except KeyError:
            print(class_nexist)
            return

        if len(args) == 1:
            print(id_missing)
            return

        key = f"{args[0]}.{args[1]}"
        all_inst = storage.all()
        try:
            print(all_inst[key])
        except Exception:
            print(inst_missing)

    def do_destroy(self, line=""):
        """ destroy <classname> <id>
        deletes the given instance `can't be reverted` """
        args = line.split()
        if len(args) == 0:
            print(class_missing)
            return

        try:
            class_obj = globals()[args[0]]
        except KeyError:
            print(class_nexist)
            return

        if len(args) == 1:
            print(id_missing)
            return

        key = f"{args[0]}.{args[1]}"
        all_inst = storage.all()
        try:
            # print(storage.__objects)
            all_inst.pop(key)
            storage.save()
        except Exception:
            print(inst_missing)

    def do_all(self, line):
        """ all <classname>
        shows all the instance of the <classname>/the all classes
        if <classname> isn't specified """
        all_inst = storage.all()
        print(all_inst)         # GDB
        if line:
            class_name = line.split()[0]

            try:
                globals()[class_name]
            except KeyError:
                print(class_nexist)
                return

            pattern = re.compile(rf"{class_name}\.\w+")
            for key, value in all_inst.items():
                if pattern.match(key):
                    print(value)
        else:
            for key, value in all_inst.items():
                print(value)

    def do_update(self, line):
        """ update <class name> <id> <attribute name> <attribute> <value>
        updates an attribute in a specific classname by a given value"""
        args = shlex.split(line)    # this splits the line respecting "--"
        if len(args) == 0:
            print(class_missing)
            return

        try:
            globals()[args[0]]
        except KeyError:
            print(class_nexist)
            return

        if len(args) == 1:
            print(id_missing)
            return

        all_inst = storage.all()
        key = f"{args[0]}.{args[1]}"
        try:
            cur = all_inst[key]
        except KeyError:
            print(inst_missing)
            return

        if len(args) == 2:
            print(attr_name_missing)
            return

        if args[2] in ['created_at', 'updated_at', 'id']:
            return

        if len(args) == 3:
            print(attr_value_missing)
            return

        # cur.__dict__[args[2]] = str(args[3])
        setattr(cur, args[2], args[3])
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
