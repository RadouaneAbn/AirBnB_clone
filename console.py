#!/usr/bin/env python3
# a program that contains the entry point of the command interpretter
######################
import cmd


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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
