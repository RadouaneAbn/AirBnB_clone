#!/usr/bin/env python3
# a program that contains the entry point of the command interpretter
######################
import cmd
import re
import shlex
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.place import Place
from models.state import State
from models import storage

CREATE = 1

class_missing = "** class name missing **"
class_nexist = "** class doesn't exist **"
id_missing = "** instance id missing **"
inst_missing = "** no instance found **"
attr_name_missing = "** attribute name missing **"
attr_value_missing = "** value missing **"

def extract(line):
    cmd, name, args = None, None, None

    # this next line check for input fomat ==> <class_name>.command(args)
    result = re.match(r'^\s*(\w+)\.(\w+)\((?:(\".*\"))?\)\s*$', line)
    if result:
        name = result.group(1)
        cmd = result.group(2)
        args = result.group(3)
        
    # this next two line cleans the input
    # Example: ("test", "the", "cleaner method")
    #        ==> 'test the "cleaner method"' 
    if args:
        args = args.replace(',', '')
        args = re.sub(r'"([^"\s]*)"', r'\1', args)

    # if not match is found the return will be None, None, None
    return cmd, name, args

def Not_In_Class_List(class_name):
    if class_name in globals():
        return False
    return True

def class_check(args):
    if len(args) == 0:
        print(class_missing)
        return False

    class_name = args[0]
    if class_name not in globals():
        print(class_nexist)
        return False

    return True

def id_check(args, instances):
    if len(args) == 1:
        print(id_missing)
        return False
    
    key = f"{args[0]}.{args[1]}"
    if key not in instances.keys():
        print(inst_missing)
        return False
    
    return True

def attribute_check(args):
    if len(args) == 2:
        print(attr_name_missing)
        return False
    
    if args[2] in ['created_at', 'updated_at', 'id']:
        return False
    
    if len(args) == 3:
        print(attr_value_missing)
        return False
    
    return True

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
        args = line.split()
        if not class_check(args):
            return

        class_obj = globals()[args[0]]
        new_obj = class_obj()
        new_obj.save()
        print(new_obj.id)


    def do_show(self, line):
        """ show <classname> <id>
        print string representation of the instance """

        args = line.split()
        all_inst = storage.all()
        if not class_check(args): return
        if not id_check(args, all_inst): return

        key = f"{args[0]}.{args[1]}"
        print(all_inst[key])


    def do_destroy(self, line):
        """ destroy <classname> <id>
        deletes the given instance `can't be reverted` """

        args = line.split()
        all_inst = storage.all()
        if not class_check(args): return
        if not id_check(args, all_inst): return

        key = f"{args[0]}.{args[1]}"
        all_inst.pop(key)
        storage.save()


    def do_all(self, line):
        """ all <classname>
        shows all the instance of the <classname>/the all classes
        if <classname> isn't specified """

        all_inst = storage.all()
        args = line.split()
        obj_list = []
        if line:
            if not class_check(args): return
            attr = f"{line.split()[0]}\.\w+"
        else:
            attr = ".*"
        pattern = re.compile(attr)

        for key, value in all_inst.items():
            if pattern.match(key):
                obj_list.append(str(value))

        print(obj_list)


    def do_update(self, line):
        """ update <class name> <id> <attribute name> <attribute> <value>
        updates an attribute in a specific classname by a given value"""

        args = shlex.split(line)    # this splits the line respecting "quotes"
        all_inst = storage.all()
        print("all fine")

        if not class_check(args): return
        if not id_check(args, all_inst): return
        if not attribute_check(args): return

        key = f"{args[0]}.{args[1]}"
        wanted_inst = all_inst[key]
        setattr(wanted_inst, args[2], args[3])
        storage.save()


    def do_count(self, name):
        """ Print the count of existing class instances """

        list_inst = storage.all()
        class_list = [key for key in list_inst.keys() if name in key]
        print(len(class_list))


    def default(self, line):
        """ Handles the commandes like this <class_name>.command(args) """

        function_list = {"all": self.do_all,
                         "count": self.do_count,
                         "show": self.do_show,
                         "destroy": self.do_destroy,
                         "update": self.do_update}

        cmd, class_name, args = extract(line)
        if not cmd and not class_name and not args:
            print("*** Unknown syntax: " + line)
            return

        final_arg = f"{class_name} {args}" if args else f"{class_name}"
        return function_list[cmd](final_arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
