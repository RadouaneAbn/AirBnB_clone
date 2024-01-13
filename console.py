#!/usr/bin/env python3
# a program that contains the entry point of the command interpretter
######################
import cmd
import re
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.place import Place
from models.state import State
from models import storage


class HBNBCommand(cmd.Cmd):
    """ the console interpreter """
    prompt = "(hbnb) "

    # macros ---------------------------------
    class_missing = "** class name missing **"
    class_nexist = "** class doesn't exist **"
    id_missing = "** instance id missing **"
    inst_missing = "** no instance found **"
    attr_name_missing = "** attribute name missing **"
    attr_value_missing = "** value missing **"

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
            Create a new instance from the <classname>
        """
        args = line.split()
        if not self.class_check(args):
            return

        class_obj = globals()[args[0]]
        new_obj = class_obj()
        new_obj.save()
        print(new_obj.id)

    def do_show(self, line):
        """ show <classname> <id>
            print string representation of the instance
        """
        args = line.split()
        all_inst = storage.all()
        if not self.class_check(args):
            return
        if not self.id_check(args, all_inst):
            return

        key = f"{args[0]}.{args[1]}"
        print(all_inst[key])

    def do_destroy(self, line):
        """ destroy <classname> <id>
            deletes the given instance `can't be reverted`
        """
        args = line.split()
        all_inst = storage.all()
        if not self.class_check(args):
            return
        if not self.id_check(args, all_inst):
            return

        key = f"{args[0]}.{args[1]}"
        all_inst.pop(key)
        storage.save()

    def do_all(self, line):
        """ all <classname>
            shows all the instance of the <classname>/the all classes
            if <classname> isn't specified
        """
        all_inst = storage.all()
        args = line.split()
        obj_list = []
        if line:
            if not self.class_check(args):
                return
            attr = rf"{line.split()[0]}\.\w+"  # to get a specific class
        else:
            attr = ".*"  # to get all classes
        pattern = re.compile(attr)

        for key, value in all_inst.items():
            if pattern.match(key):
                obj_list.append(str(value))

        print(obj_list)

    def do_update(self, line):
        """ update <class name> <id> <attribute> <value>
            updates an attribute in a specific classname by a given value
        """
        # print(line)
        if not line:
            print(self.class_missing)
            return

        parsed_line = re.match(r'^(\S*)\s?(\S*)\s?("[^"]+"|\S*)?\s?("[^"]+"|\S*)', line)
        args = list(parsed_line.groups())

        # args = shlex.split(line)  # this splits the line respecting "quotes"
        # print(args)
        all_inst = storage.all()
        # data_type = int

        if not self.class_check(args):
            return
        if not self.id_check(args, all_inst):
            return
        if not self.attribute_check(args):
            return
        
        key, value = args[2], args[3]
 
        try:
            value = eval(value)
        except Exception:
            pass
        

        search_key = f"{args[0]}.{args[1]}"
        wanted_inst = all_inst[search_key]
        # value = expected_type(value)
        setattr(wanted_inst, key, value)
        wanted_inst.save()

    def count(self, name):
        """ Print the count of existing class instances """
        list_inst = storage.all()
        class_list = [key for key in list_inst.keys() if name in key]
        print(len(class_list))

    def default(self, line):
        """ Handles the commandes like this <class_name>.command(args) """
        function_list = {"all": self.do_all,
                         "count": self.count,
                         "show": self.do_show,
                         "destroy": self.do_destroy,
                         "update": self.do_update,
                         "create": self.do_create}

        cmd, args = self.extract(line)
        if not args:
            print("*** Unknown syntax: " + line)
            return
        # print(args)
        for arg in args:
            # print(arg)
            function_list[cmd](arg)

        return

    # helpers ------------------------------------------------
    def extract(self, line):
        cmd, name, args = None, None, None
        arg_list = []
        final_args = []

        # this next line check for input fomat ==> <class_name>.command(args)
        result = re.match(r'^\s*(\w+)\.(\w+)\((?:([{"\']?.*["\'}]?))?\)\s*$', line)
        if result:
            name = result.group(1)
            cmd = result.group(2)
            args = result.group(3)

            # this next two line cleans the input
            # Example: ("test", "the", "cleaner method")
            #        ==> 'test the "cleaner method"'
        if args:
            result_2 = re.match(r'"?([^"]\S+)"?, {(.+)}', args)
        if cmd == "update" and result_2:
            # print("match found")
            id = result_2.group(1)
            patt = re.compile(r'("[^"]+"|\S+):\s("[^"]+"|[^, ]+)')
            matches = patt.findall(result_2.group(2))
            for match in matches:
                key = match[0]
                value = match[1]
                final_args.append(f"{id} {key} {value}")

        elif args:
            args = args.replace(',', '')
            final_args.append(re.sub(r'(["\'])([^"\s]*)\1', r'\2', args))
        # print("final_args>> ", end="")
        # print(final_args)
        if final_args:
            for arg in final_args:
                arg_list.append(f"{name} {arg}" if arg else f"{name}")
        elif name:
            arg_list.append(f"{name}")

        # print("arg_list>> ", end="")
        # print(arg_list)
        return cmd, arg_list

    def class_check(self, args):
        # print(args[0])
        args[0] = args[0].strip('"')
        if args[0] not in globals():
            print(self.class_nexist)
            return False

        return True


    def id_check(self, args, instances):
        if len(args) == 1:
            print(self.id_missing)
            return False
        
        args[1] = args[1].strip('"')
        key = f"{args[0]}.{args[1]}"
        if key not in instances.keys():
            print(self.inst_missing)
            return False

        return True


    def attribute_check(self, args):
        if len(args) == 2:
            print(self.attr_name_missing)
            return False

        args[2] = args[2].strip('"')
        if args[2] in ['created_at', 'updated_at', 'id']:
            return False

        if not args[3]:
            print(self.attr_value_missing)
            return False

        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
