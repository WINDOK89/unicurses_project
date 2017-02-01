# -*- coding: utf-8 -*-
import ast
from unicurses import *
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


class PyLakeClient(StandardTerminal):
    """
    inherit from Standard terminal, only the function are added to it
    """
    def __init__(self):
        """
        contructor, we start first with specific variable of child class
        """

        """call to inherit constructor"""
        StandardTerminal.__init__(self)

        """get PyLakeDDriver connection"""
        self.MyLake=PyLakeDriver("wintell", "wintell347", "148.251.51.21", DefaultDir="wintell/SR4")

        """set memory for tag"""
        self.TagMemory=TagMemory(self.MyLake.browse_directory())
        self.DirMemory=DirMemory(self.MyLake.get_tag_directories())

        """Tag choice manager"""
        self.ChoiceWindow = DisplayWindow(self.stdscr, self.InputWindow)

        """dir choice manager"""
        self.DirChoiceWindow = DisplayWindow(self.stdscr, self.InputWindow)

        """arrange element"""
        top_panel(self.OutputWindow.panel)
        #bottom_panel(self.ChoiceWindow.panel)
        #bottom_panel(self.DirChoiceWindow.panel)

        """start loop"""
        self.start_loop()

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

        """terminate app if loop over"""
        endwin()

    def manage_buffer(self, key):
        """
        overwrite inherit method to add some function (select tag and dir)
        :param key: the input key given
        :return:
        """

        """to displlay at top display screen"""
        top_panel(self.OutputWindow.panel)
        bottom_panel(self.ChoiceWindow.panel)
        bottom_panel(self.DirChoiceWindow.panel)
        self.OutputWindow.show_changes()

        """manage key tab"""
        if (key == 9):
            """reinitialize the quit request flag"""
            self.ChoiceWindow.quitRequest = True

            PosTag, lastSection = self.TagMemory.get_next(self.Buffer)
            if len(PosTag) == 1:
                self.Buffer = self.Buffer + list(PosTag[0])[len(lastSection):]
                self.InputWindow.PosCur = len(self.InputWindow.message) + len(self.Buffer)
            elif len(PosTag) > 1:
                self.ChoiceWindow.clear_display()
                top_panel(self.ChoiceWindow.panel)
                bottom_panel(self.OutputWindow.panel)
                bottom_panel(self.DirChoiceWindow.panel)
                for elt in PosTag:
                    self.ChoiceWindow.add_text(" --> {}".format(elt), color=7, attribute=A_REVERSE)
                self.ChoiceWindow.show_changes()
            else:
                pass

        elif (key == KEY_BTAB):
            """reinitialize the quit request flag"""
            self.ChoiceWindow.quitRequest = True

            PosTag, lastSection = self.DirMemory.get_next(self.Buffer)
            if len(PosTag) == 1:
                self.Buffer = self.Buffer + list(PosTag[0])[len(lastSection):]
                self.InputWindow.PosCur = len(self.InputWindow.message) + len(self.Buffer)
            elif len(PosTag) > 1:
                self.DirChoiceWindow.clear_display()
                top_panel(self.DirChoiceWindow.panel)
                bottom_panel(self.OutputWindow.panel)
                bottom_panel(self.ChoiceWindow.panel)
                for elt in PosTag:
                    self.DirChoiceWindow.add_text(" --> {}".format(elt), color=8, attribute=A_REVERSE)
                self.DirChoiceWindow.show_changes()
            else:
                pass

        else:
            StandardTerminal.manage_buffer(self,key)

def string_to_list_tuple_dict(s):
    try:
        ret=ast.literal_eval(s)
    except:
        return False
    else:
        return ret

if __name__ == "__main__":
    a = PyLakeClient()
