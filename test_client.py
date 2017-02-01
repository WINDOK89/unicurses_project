# -*- coding: utf-8 -*-
import ast
from PyLakeDriver import *
from ModuleStdTerminal import *

class TagMemory(DirMemory):
    """
    This class is inheriting from DirMemory because the input is not directly a list but a dictionnary
    we will loop over the dict to create the list first, before calling the constructor
    The end purpose is to give tag name possibility with key tab
    """
    def __init__(self, dic):
        """
        the constructor
        :param dic: the dict containing what we need
        """

        """The final tag name list initialisation"""
        TagNameList=[]

        """the dic is coming from pylakedriver fct which return false if a problem happens"""
        if dic != False:

            """we take the tag names from the dic and add it to tag possibility list"""
            for IL1 in dic.values():
                TagNameList.append(IL1['name'])

        """now all condition are ok to call DirMemory constructor passing a list and not a dict"""
        DirMemory.__init__(self,TagNameList)


class PyLakeClient():
    """
    inherit from Standard terminal, only the function are added to it
    """
    def __init__(self):
        """
        contructor, we start first with specific variable of child class
        """

        stdTerminal=StandardTerminal()
        stdTerminal.start_loop()

    def start_loop(self):
        """
        redefinition of start loop to have the current directory in the cmd message
        :return:
        """

        while (self.cmd != "quit"):
            key = self.InputWindow.get_char(message=" {} # Terminal >> ".format(self.MyLake.DefaultDir), buf="".join(self.Buffer))
            self.manage_buffer(key)
            mvaddstr(0, 0, "   ")
            mvaddstr(0, 0, str(key))


def string_to_list_tuple_dict(s):
    try:
        ret=ast.literal_eval(s)
    except:
        return False
    else:
        return ret

if __name__ == "__main__":
    a = PyLakeClient()
