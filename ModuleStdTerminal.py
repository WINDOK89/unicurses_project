from unicurses import *


def color_init():
    """
    Initialization of color par
    :return: no return
    """
    init_pair(1, COLOR_WHITE, COLOR_BLACK)
    init_pair(2, COLOR_RED, COLOR_BLACK)
    init_pair(3, COLOR_CYAN, COLOR_BLACK)
    init_pair(4, COLOR_RED, COLOR_CYAN)
    init_pair(5, COLOR_YELLOW, COLOR_BLACK)
    init_pair(6, COLOR_GREEN, COLOR_BLACK)
    init_pair(7, COLOR_RED, COLOR_WHITE)


class DisplayWindow():
    """
    This class allow to create and manage a display area (full size)
    """

    def __init__(self, stdscr, cmdscr, WinType="Primary"):
        """
        constructor

        :param stdscr: the main screen of the appplication
        :param cmdscr: the input screen of the application
        :param WinType: 'primary' per default, nothing else at the moment
        """

        """get main screen dimension than delete the link (not needed anymore)"""
        self.max_x = stdscr.getmaxyx()[1] - 1
        self.max_y = stdscr.getmaxyx()[0] - 1
        del stdscr

        """get dimension of the window we will create (dimension so the display area is within the main screen margin"""
        self.Xlength = self.max_x - 3
        self.Ylength = self.max_y - 5

        """for future evolution, create more wintype, with type 'primary', the window cover full area"""
        if WinType == "Primary":
            self.window = newwin(self.Ylength, self.Xlength, 2, 2)

        """keep track of the input command window"""
        self.cmdscr = cmdscr

        """create the panel"""
        self.panel = new_panel(self.window)

        """keep track of the cursor position within self.window"""
        self.Xpos = 0
        self.Ypos = 0

        """this flag is used to allow the display to propose 'quit' or 'next', the flag must be put to True oncce the main app has finished"""
        self.quitRequest = True

        """call to this function to show the changes at declaration"""
        self.show_changes()

    def clear_display(self):
        """
        The window is clear
        the position is initialized

        :return:
        """
        wclear(self.window)
        self.Ypos = 0
        self.Xpos = 0

    def add_line(self, message, attribute=A_NORMAL, color=1):
        """
        add the line to the display, upgarde cursor position (add tab)

        :param message: the string to add
        :param attribute: the special attributes
        :param color: the color pair number
        :return:
        """
        waddstr(self.window, message, color_pair(color) + attribute)

        """we takes the new position"""
        NewX = getyx(self.window)[1]
        NewY = getyx(self.window)[0]

        """we set the new position and update"""
        self.Xpos = 0
        self.Ypos = NewY + 1
        self.show_changes()

    def add_text(self, message, color=1, attribute=A_NORMAL):
        """
        the main app use this function to send a request for display
        the function place the cursor at the registered position
        the function check if there is enough space and start command loop if needed

        :param message: The message to add
        :param color: the color pair number for the message
        :param attribute: the special attribute
        :return:
        """

        """plaace the cursor at the end of last inserted string + break"""
        wmove(self.window, self.Ypos, self.Xpos)

        """if thee new position is out of range, wee don't upgrade, if not, we upgrade"""
        """we count the number of lines we need to add the message"""
        if int(len(message) / self.Xlength) + self.Ypos > self.Ylength - 1:

            """if we need too much lines, we set this flag to start the loop"""
            Finished = True

            """start loop decision (quit or next)"""
            """two condition to have the loop running"""
            while (Finished and self.quitRequest):

                """we request the cmd from input window to stop or update"""
                key = self.cmdscr.get_char(message=" 'q' for quit, 'enter' for next >> ", buf="")

                """if user request 'quit'"""
                if (chr(key) == 'q'):
                    """set input cmd cursor back to start"""
                    self.cmdscr.PosCur = -1

                    """set this flag to False to break the loop, this flag will be rinitialized in the main app"""
                    self.quitRequest = False

                """if user request 'next'"""
                if (key == 10):
                    """clear window and cursor"""
                    self.clear_display()

                    """we try to add the message"""
                    self.add_line(message, attribute=attribute, color=color)

                    """finished loop"""
                    Finished = False

                    """set cmd window cursor back to start"""
                    self.cmdscr.PosCur = -1


        else:

            """we try to add the message"""
            self.add_line(message, attribute=attribute, color=color)

    def show_changes(self):
        """
        to update display

        :return:
        """
        update_panels()
        doupdate()
