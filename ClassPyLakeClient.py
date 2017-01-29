# -*- coding: utf-8 -*-
from unicurses import *
from PyLakeDriver import *
import csv


def color_init():
    init_pair(1, COLOR_WHITE, COLOR_BLACK)
    init_pair(2, COLOR_RED, COLOR_BLACK)
    init_pair(3, COLOR_BLUE, COLOR_BLACK)
    init_pair(4, COLOR_RED, COLOR_CYAN)
    init_pair(5, COLOR_YELLOW, COLOR_BLACK)


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

        """init buffer and cmd"""
        self.Buffer = []
        self.cmd = ""

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

        """start loop"""
        while (self.cmd != "quit"):
            key = self.InputWindow.get_char(buf="".join(self.Buffer))
            self.manage_buffer(key)
            mvaddstr(0, 0, "   ")
            mvaddstr(0, 0, str(key))

        """terminate app"""
        endwin()

    def manage_buffer(self, key):

        """check if enter pressed"""
        if (key == 10):
            self.cmd = "".join(self.Buffer)
            self.Buffer = []
            self.InputWindow.PosCur = -1
            """manage cmd from here"""
            self.cmd_manager()

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

        """help menu"""
        if  self.cmd=="hh":
            mvaddstr(0,10,"help")


if __name__ == "__main__":
    a = PyLakeClient()
