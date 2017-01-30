# -*- coding: utf-8 -*-
from unicurses import *
from PyLakeDriver import *
import csv


def color_init():
    init_pair(1, COLOR_WHITE, COLOR_BLACK)
    init_pair(2, COLOR_RED, COLOR_BLACK)
    init_pair(3, COLOR_CYAN, COLOR_BLACK)
    init_pair(4, COLOR_RED, COLOR_CYAN)
    init_pair(5, COLOR_YELLOW, COLOR_BLACK)
    init_pair(6, COLOR_GREEN, COLOR_BLACK)


class DisplayWindow():
    def __init__(self, stdscr, cmdscr):
        self.max_x = stdscr.getmaxyx()[1] - 1
        self.max_y = stdscr.getmaxyx()[0] - 1
        self.Xlength = self.max_x - 3
        self.Ylength = self.max_y - 5

        del stdscr

        self.window = newwin(self.max_y - 5, self.max_x - 3, 2, 2)
        self.cmdscr = cmdscr

        self.panel = new_panel(self.window)

        self.Xpos = 0
        self.Ypos = 0

        self.quitRequest=True

        self.show_changes()

    def clear_display(self):
        wclear(self.window)
        self.Ypos = 0
        self.Xpos = 0

    def add_line(self, message, attribute=A_NORMAL, color=1):
        waddstr(self.window, message, color_pair(color)+attribute)

        """we takes the new position"""
        NewX = getyx(self.window)[1]
        NewY = getyx(self.window)[0]

        """we set the new position and update"""
        self.Xpos = 0
        self.Ypos = NewY + 1
        self.show_changes()

    def add_text(self, message, color=1, attribute=A_NORMAL):

        """set the positioon like it should be"""
        wmove(self.window, self.Ypos, self.Xpos)

        """if thee new position is out of range, wee don't upgrade, if not, we upgrade"""
        if int(len(message) / self.Xlength) + self.Ypos > self.Ylength - 1:
            Finished = True
            while (Finished and self.quitRequest):
                """we request the cmd to stop or update"""
                key = self.cmdscr.get_char(message=" 'q' for quit, 'enter' for next >> ", buf="")

                if (chr(key) == 'q'):
                    """quit loop without update"""
                    self.cmdscr.PosCur = -1
                    self.quitRequest=False

                if (key == 10):
                    """update"""
                    wclear(self.window)
                    self.Xpos = 0
                    self.Ypos = 0

                    """we try to add the message"""
                    self.add_line(message, attribute=attribute, color=color)

                    """finished loop"""
                    Finished = False
                    self.cmdscr.PosCur = -1


        else:
            """we try to add the message"""
            self.add_line(message, attribute=attribute, color=color)

    def show_changes(self):
        update_panels()
        doupdate()


class CmdWindow():
    def __init__(self, stdscr):
        self.max_x = stdscr.getmaxyx()[1] - 1
        self.max_y = stdscr.getmaxyx()[0] - 1
        del stdscr

        self.window = newwin(1, self.max_x - 5, self.max_y - 1, 2)
        self.panel = new_panel(self.window)

        """super critical, this will enable arrow key to be equal to KEY_LEFT,.."""
        keypad(self.window, True)

        """to know where start the buf"""
        self.BufStart = 0

        """to know if the cursor position has to change"""
        self.PosCur = -1

        """keep track of the message"""
        self.message = ""

        """show window"""
        self.show_changes()

    def get_char(self, message=" Enter a command >> ", buf=""):

        """ask for the command"""
        wmove(self.window, 0, 0)
        waddstr(self.window, message, color_pair(2) + A_BOLD)

        """keep track of the message"""
        self.message = message

        """keep track of buffer position"""
        self.BufStart = len(message)

        """add the buffer"""
        waddstr(self.window, buf, color_pair(5) + A_BOLD)

        """show changes in sub window"""
        self.show_changes()

        """cursor managemment"""
        if (self.PosCur == -1):
            pass
        else:
            wmove(self.window, 0, self.PosCur)

        """get cursor position before clear"""
        self.PosCur = getyx(self.window)[1]

        """request character"""
        cmd = wgetch(self.window)

        """clear full content"""
        wclear(self.window)

        """return command"""
        return cmd

    def show_changes(self):
        update_panels()
        doupdate()


class PyLakeClient():
    def __init__(self):

        """intialization"""
        self.stdscr = initscr()

        """color init"""
        start_color()
        color_init()

        """allow special keey"""
        """super critical, this will enable arrow key to be equal to KEY_LEFT,.."""
        keypad(self.stdscr, True)

        """get max dim"""
        self.MaxX = getmaxyx(self.stdscr)[1] - 1
        self.MaxY = getmaxyx(self.stdscr)[0] - 1

        """set cmd memory"""
        self.cmdMemory=[]
        self.cmdMemoryIndex=0
        self.cmdEnterFlag=True

        """init buffer and cmd"""
        self.Buffer = []
        self.copyBuffer = []
        self.cmd = ""

        """get PyLakeDDriver connection"""
        self.MyLake=PyLakeDriver("wintell", "wintell347", "148.251.51.21", DefaultDir="wintell/SR4")

        """draw  separtion line between content and command"""
        move(self.MaxY - 2, 2)
        hline(ACS_HLINE, self.MaxX - 2)
        move(self.MaxY, 2)
        hline(ACS_HLINE, self.MaxX - 2)
        move(1, 2)
        hline(ACS_HLINE, self.MaxX - 2)
        move(1, 1)
        vline(ACS_VLINE, self.MaxY)
        move(1, self.MaxX - 1)
        vline(ACS_VLINE, self.MaxY)

        """cmd window"""
        self.InputWindow = CmdWindow(self.stdscr)
        self.OutputWindow = DisplayWindow(self.stdscr, self.InputWindow)

        """start loop"""
        while (self.cmd != "quit"):
            key = self.InputWindow.get_char(message=" {} # Terminal >> ".format(self.MyLake.DefaultDir), buf="".join(self.Buffer))
            self.manage_buffer(key)
            mvaddstr(0, 0, "   ")
            mvaddstr(0, 0, str(key))

        """terminate app"""
        endwin()

    def manage_buffer(self, key):
        """"""
        """copy buffer if we are not select memory"""
        if self.cmdEnterFlag:
            self.copyBuffer=self.Buffer
        self.cmdEnterFlag=True

        """check if enter pressed"""
        if (key == 10):
            self.cmd = "".join(self.Buffer)
            self.cmdMemory.append(self.cmd)
            self.cmdMemoryIndex = 0
            self.Buffer = []
            self.InputWindow.PosCur = -1
            """manage cmd from here"""
            self.cmd_manager()

        elif (key == KEY_UP):

            if ((self.cmdMemoryIndex + 1) <= len(self.cmdMemory)) and (self.cmdMemoryIndex>=0) and len(self.cmdMemory) != 0:
                self.cmdMemoryIndex += 1
                self.Buffer = list(self.cmdMemory[len(self.cmdMemory)-self.cmdMemoryIndex])
                self.InputWindow.PosCur = len(self.InputWindow.message)+len(self.Buffer)
            self.cmdEnterFlag = False

        elif (key == KEY_DOWN):

            if (self.cmdMemoryIndex >= 1) and ((self.cmdMemoryIndex-1) < len(self.cmdMemory)) and len(self.cmdMemory) != 0:
                self.cmdMemoryIndex -= 1
                if self.cmdMemoryIndex==0:
                    self.Buffer=self.copyBuffer
                    self.InputWindow.PosCur = len(self.InputWindow.message) + len(self.Buffer)
                else:
                    self.Buffer = list(self.cmdMemory[len(self.cmdMemory)-self.cmdMemoryIndex])
                    self.InputWindow.PosCur = len(self.InputWindow.message)+len(self.Buffer)
            self.cmdEnterFlag = False


        elif (key == KEY_BACKSPACE):  # check if backspace key pressed
            # check if len(buf) > 0 to avoid li[-1]
            if (len(self.Buffer) > 0 and self.InputWindow.PosCur > len(self.InputWindow.message)):
                del self.Buffer[self.InputWindow.PosCur - len(self.InputWindow.message) - 1]
                self.InputWindow.PosCur -= 1

        elif (key == KEY_LEFT):
            if (self.InputWindow.PosCur > self.InputWindow.BufStart):
                self.InputWindow.PosCur -= 1

        elif (key == KEY_RIGHT):
            if (len(self.Buffer) + len(self.InputWindow.message) > self.InputWindow.PosCur):
                self.InputWindow.PosCur += 1

        elif (key == KEY_UP):
            pass

        elif (key == 330):
            if ((self.InputWindow.PosCur - len(self.InputWindow.message) < len(self.Buffer))):
                del self.Buffer[self.InputWindow.PosCur - len(self.InputWindow.message)]

        elif (key == 9):
            pass

        elif (key == KEY_DOWN):
            pass

        else:
            self.Buffer.insert(self.InputWindow.PosCur - len(self.InputWindow.message), chr(key))
            self.InputWindow.PosCur += 1

    def cmd_manager(self):

        """"""

        """get cmd list"""
        cmdlist=self.cmd.split(" :")

        """help menu"""
        if cmdlist[0] == "help":
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("HELP CONTENT", color=2, attribute=A_BOLD+A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'quit':", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> exit terminal")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'help':", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> display help content")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'gd :%p1':", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> display all subdirectory from '%p1'")
            self.OutputWindow.add_text("    --> '%p1' : root directory, 'wintell/' per default")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'ad :%p1':", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> add subdirectory '%p1' to root 'wintell/'")
            self.OutputWindow.add_text("    --> '%p1' : directory name to create")
            self.OutputWindow.add_text("    --> Return: the new directory name is returned")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'sdd :%p1':", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> set default directory to '%p1' ")
            self.OutputWindow.add_text("    --> '%p1' : directory name to set")
            self.OutputWindow.add_text("    --> Return: the new directory name is returned")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'at :%p1 :%p2 :%p3 :%p4 :%p5 :%p6':", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> create tag ")
            self.OutputWindow.add_text("    --> '%p1' : tag name ")
            self.OutputWindow.add_text("    --> '%p2' : tag type ")
            self.OutputWindow.add_text("    --> '%p3' : tag unit ")
            self.OutputWindow.add_text("    --> '%p4' : tag description ")
            self.OutputWindow.add_text("    --> '%p5' : tag title ")
            self.OutputWindow.add_text("    --> '%p6' : tag directory, if none existing, it is created, it is optionnal ")
            self.OutputWindow.add_text("    --> Return: the new tag characteristics are returned")

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest=True

        elif cmdlist[0] == "gd":   #get driectories
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("GET DIRECTORIES", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist)==1:
                cmdlist.append("")
            """normally every cmd should be two comp"""
            if len(cmdlist)==2:
                DirList = self.MyLake.get_tag_directories(TagDirParam="{}/{}".format("wintell",cmdlist[1]))
                if DirList != False:
                    self.OutputWindow.add_text("    --> wintell")
                    for elt in DirList:
                        finalStr=""
                        eltSplit=elt.split('/')
                        for elt2 in eltSplit:
                            finalStr += "    "

                        self.OutputWindow.add_text("{}--> {}".format(finalStr,eltSplit[len(eltSplit)-1]))
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "gtl":   #get tag list
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("GET TAG LIST", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist)==1:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist)==2:
                TagList = self.MyLake.get_tag_list(TagDirParam="{}".format(cmdlist[1]))
                if TagList != False:
                    for elt in TagList:
                        finalStr=""
                        eltSplit=elt.split('/')
                        for elt2 in eltSplit:
                            finalStr += "    "

                        self.OutputWindow.add_text("{}--> {}".format(finalStr,eltSplit[len(eltSplit)-1]))
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "at":   #add tag
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("ADD TAG", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""

            """no default dir"""
            if len(cmdlist) == 6:
                cmdlist.append(self.MyLake.DefaultDir)

            """manage if user send no parameter"""
            if len(cmdlist)<6:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            elif len(cmdlist)==7: #no default dir given
                TagList = self.MyLake.create_tags(cmdlist[1], TagType=cmdlist[2], TagUnit=cmdlist[3], TagDescription=cmdlist[4], TagTitle=cmdlist[5], TagDirParam="{}".format(cmdlist[6]))
                if TagList != False:
                    self.OutputWindow.add_text("    --> New tag '{}' in directory '{}'".format(cmdlist[1],cmdlist[6]))
                    self.OutputWindow.add_text("        --> Unit: '{}'".format(cmdlist[2]))
                    self.OutputWindow.add_text("        --> Type: '{}'".format(cmdlist[3]))
                    self.OutputWindow.add_text("        --> Description: '{}'".format(cmdlist[4]))
                    self.OutputWindow.add_text("        --> Title: '{}'".format(cmdlist[5]))
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR WRONG INPUT!!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "sdd":   #set default directory
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("SET DEFAULT DIRECTORY", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""

            """normally every cmd should be two comp"""
            if len(cmdlist)==2:
                self.OutputWindow.add_text("   --> Former directory: {}".format(self.MyLake.DefaultDir))
                self.MyLake.DefaultDir=cmdlist[1]
                self.OutputWindow.add_text("   --> new directory set: {}".format(self.MyLake.DefaultDir))

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "ad":   #add directory
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("ADD DIRECTORY", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """check parameter is there"""
            if len(cmdlist)==2:
                if self.MyLake.create_directory(cmdlist[1]):
                    self.OutputWindow.add_text("    --> Directory '{}' has been created successfully".format(cmdlist[1]), color=6)
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER !!", color=2)
            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP2 !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        else:
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True


if __name__ == "__main__":
    a = PyLakeClient()
