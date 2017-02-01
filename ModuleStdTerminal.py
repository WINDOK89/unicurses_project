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
    init_pair(8, COLOR_BLUE, COLOR_WHITE)


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


class DirMemory():
    """
    initialy this class was done for pylakeclient to return autocompletion function of directories
    But it can be used simply to return autocompletion over a list
    """
    def __init__(self, DirList):
        """
        contructor of the class
        :param DirList: the list of all possible input
        """

        """keep track of all possibile input"""
        self.DirNameList=DirList

    def get_next(self, BufFromApp):
        """
        the function return a list containing the reduced possibility all containing at begin the BufFromApp

        :param BufFromApp: what the user typed in at begin of cmd or after ' :'
        :return: list empty if no possibility, list with one possibility if the common part of all possibilities is longer than what the usser typed already in, list of several possibilities if user input is as long as the common parts
        """

        """the user input buffer is converted into string"""
        cmd = "".join(BufFromApp)

        """we split parameter adn command (so we can propose choice on cmd and after param"""
        cmdSplit = cmd.split(" :")

        """we insulate the ssection where we want to add a possibility"""
        lastSection = cmdSplit[len(cmdSplit) - 1]

        """initialisation of lret (list of all reduced posisbilities"""
        lret = []

        """loop over all possibilities to insulate all which contains lastsection"""
        for elt in self.DirNameList:

            """if the possibility start with what the user typed in, we put it in lret"""
            if elt.startswith(lastSection):
                lret.append(elt)

        """Next variable will be used to return all common char with all reduced possibilities"""
        FinalLRet = []

        """we check common part only if there are several possibilities"""
        if len(lret) > 1:

            """we loop over reduced possibilities"""
            for i, letter in enumerate(list(lret[0])):

                """flag will be used to break the loop"""
                flag = True

                """we loop over the first possibility 's characters"""
                for elt in lret:

                    """if the char is not present in the actual possibility, we set flag to false(char cannot be in list of common char)"""
                    if list(elt)[i] != letter:
                        flag = False

                """if the char is present, in all possibilities, we add it in the list containing all common char, if not, we break the loop"""
                if flag == True:
                    FinalLRet.append(letter)
                else:
                    break

        """if the common part is longer than user input, we retrun a list with the string common part only (add to the cmd screen)"""
        """else we return all possibilities"""
        """last section is return too to add the possibility missing section to the buffer"""
        if len(FinalLRet) > len(lastSection):
            return ["".join(FinalLRet)], lastSection
        else:
            return lret, lastSection


class CmdWindow():
    """
    this class create and manage the lower part of the app where the user enter the commands
    """

    def __init__(self, stdscr):
        """
        The constructor
        :param stdscr: the main screen of the app
        """

        """get the max dim of the main screen than erase the link"""
        self.max_x = stdscr.getmaxyx()[1] - 1
        self.max_y = stdscr.getmaxyx()[0] - 1
        del stdscr

        """create the window and the panel"""
        self.window = newwin(1, self.max_x - 5, self.max_y - 1, 2)
        self.panel = new_panel(self.window)

        """super critical, this will enable arrow key to be equal to KEY_LEFT,.."""
        keypad(self.window, True)

        """to know where start the buf, because the message (part before user input) can have different length so we need this variable to know where the user start to enter cmd, initialize at 0 because there is no message yes"""
        self.BufStart = 0

        """to know if the cursor position has to change"""
        """in normal situation, the cursor follow the input of the user but if we use history cmd or if we want to move the cursoor without erase part of the command, we need to set the cursor position"""
        """if -1, nothing happen and the cursor follow input, otherwise, it will move to self.PosCur"""
        """format : '(message starts) enter a command >> (BufStart keep this position) cmd p1 p2 p(self.PosCur)'"""
        self.PosCur = -1

        """keep track of the message befor input"""
        self.message = ""

        """show window"""
        self.show_changes()

    def get_char(self, message=" Enter a command >> ", buf=""):
        """
        This function will require a key input (char by char) and manager cursor position

        :param message: what the user see before typing in
        :param buf: what is already in the buffer (user has not pressed enter yet
        :return: the input char the user gived
        """

        """ask for the command"""
        """we put teh cursor back to 0 in the input window"""
        wmove(self.window, 0, 0)

        """we add the message before user input"""
        waddstr(self.window, message, color_pair(2) + A_BOLD)

        """keep track of the message because we will need it in the main app to set cursor position or move the cursor"""
        self.message = message

        """keep track of the minimum place the cursor can go"""
        self.BufStart = len(message)

        """add the buffer (what the user has already put in"""
        waddstr(self.window, buf, color_pair(5) + A_BOLD)

        """show changes in sub window"""
        self.show_changes()

        """cursor managemment"""
        """if no change of position requested the cursor will just stay where the user write last character"""
        if (self.PosCur == -1):
            pass

        else:
            """if change requested we move where the main app has requested to"""
            wmove(self.window, 0, self.PosCur)

        """get cursor position before clear"""
        self.PosCur = getyx(self.window)[1]

        """request character"""
        cmd = wgetch(self.window)

        """clear full content after user input"""
        wclear(self.window)

        """return command"""
        return cmd

    def show_changes(self):
        """
        to upgrade display

        :return:
        """
        update_panels()
        doupdate()