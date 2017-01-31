# -*- coding: utf-8 -*-
from unicurses import *


# https://www.youtube.com/watch?v=S09WKA8K9Ek
# copy unicureses.py in unicurses folder (site packages) and erase unicurese.py from site package



def main():
    """initilize screen"""

    stdscr = initscr()

    """move(col,row) curse"""
    # move(10,10)

    """add string fct"""
    # addstr("hello world")

    """move and add string at the same time"""
    # mvaddstr(10,10,"hello")

    """some moving"""
    for i in range(1, 10):
        clear()  # to remove what is on the screen
        mvaddstr(i, i, "hello")
        getch()

    """get character fct"""
    getch()

    """when we are done, we use endwin () to close our terminal"""
    endwin()


def main2():
    stdscr = initscr()
    running = True
    while (running):
        key = getch()
        clear()
        if (key == 27):
            running = False
        mvaddstr(10, 0, "keycode was:" + str(key) + " and the key was:" + chr(key))
        move(0, 0)
    endwin()


def main3():
    stdscr = initscr()
    nocbreak()
    running = True
    while (running):
        key = getstr()
        clear()
        if (str(key.decode()) == "q"):
            running = False
        mvaddstr(10, 0, "keycode was:" + str(key) + " and the key was:" + str(key.decode()))
        move(0, 0)
    endwin()


def main4():
    stdscr = initscr()
    # attribute: https://docs.python.org/3.4/library/curses.html#module-curses
    attron(A_BOLD)
    mvaddstr(0, 0, "hello\n")
    attroff(A_BOLD)
    addstr("hello\n")
    attron(A_REVERSE)
    addstr("hello\n")
    addstr("hello\n", A_BOLD)
    attroff(A_REVERSE)
    addstr("hello\n")
    getch()

    endwin()


def main5():
    stdscr = initscr()

    """iniatize color tool"""
    start_color()
    use_default_colors()  # not necessary
    """create pair of color (text,bqckground)"""
    init_pair(1, COLOR_RED, COLOR_BLUE)

    addstr("hello\n", color_pair(1) + A_REVERSE)
    addstr("hello\n", color_pair(1))
    getch()
    endwin()


def main6():
    stdscr = initscr()

    """no echo to dont show wha we type in"""
    noecho()

    """todont see cursor"""
    curs_set(False)

    """enable color"""
    start_color()

    """get arrows key active and readable"""
    keypad(stdscr, True)

    start_color()
    running = True
    while (running):
        key = getch()
        if (key == 27):
            running = False

    endwin()


def main7():
    stdscr = initscr()

    """no echo to dont show wha we type in"""
    noecho()

    """todont see cursor"""
    curs_set(False)

    """enable color"""
    start_color()

    """get arrows key active and readable"""
    keypad(stdscr, True)

    """create subwindow"""
    window = newwin(10, 25, 0, 10)
    waddstr(window, "hello worldfgfdgfdgfdgfdgfdgdfgfdgfdgfdg")

    window2 = newwin(10, 25, 11, 10)
    waddstr(window2, "hello worldfgfdgfdgfdgfdgfdgdfgfdgfdgfdg")

    running = True
    while (running):
        key = wgetch(window2)  # using wgetch will specify the window displayed
        if (key == 27):
            running = False

    endwin()


def main8():
    stdscr = initscr()

    """no echo to dont show wha we type in"""
    noecho()

    """todont see cursor"""
    curs_set(False)

    """enable color"""
    start_color()

    """get arrows key active and readable"""
    keypad(stdscr, True)

    """create subwindow and show it"""
    window = newwin(10, 25, 0, 0)
    box(window)
    wmove(window, 1, 1)
    waddstr(window, "hello")

    running = True
    while (running):
        key = wgetch(window)  # using wgetch will specify the window displayed
        if (key == 27):
            running = False

    endwin()


def main9():
    stdscr = initscr()
    start_color()
    noecho()
    curs_set(False)
    keypad(stdscr, True)

    """get max size"""
    # to change windows size, launch the app from the file and use its parameter to change default size
    dim = getmaxyx(stdscr)
    addstr(str(dim[0]) + "es\n")
    addstr(str(dim[1]) + "\n")

    """panel tuto (doesnt work on window but ok on linux"""
    window = newwin(3, 20, 4, 4)
    box(window)
    wmove(window, 1, 1)
    waddstr(window, "hey youtube")
    panel = new_panel(window)

    window2 = newwin(3, 20, 4, 4)
    box(window2)
    wmove(window2, 1, 1)
    waddstr(window2, "heyasshole")
    panel2 = new_panel(window2)

    move_panel(panel2, 5, 5)

    top_panel(panel)  # lot of function for panel

    running = True
    while (running):
        key = getch()  # using wgetch will specify the window displayed
        if (key == 27):
            running = False
        update_panels()
        doupdate()

    endwin()

def main10():
    stdscr=initscr()
    start_color()


if __name__ == "__main__":
    main8()

    BufFromApp = list("tag11")
    cmd = "".join(BufFromApp)
    cmdSplit = cmd.split(" :")
    lastSection = cmdSplit[len(cmdSplit) - 1]
    lret = []
    for elt in ['test', 'tag11', 'tag11abc', 'tag2', 'tag2abc']:
        if elt.startswith(lastSection):
            lret.append(elt)
    FinalLRet = []
    if len(lret) > 1:
        for i, letter in enumerate(list(lret[0])):
            flag = True
            for elt in lret:
                if list(elt)[i] != letter:
                    flag = False
            if flag == True:
                FinalLRet.append(letter)
            else:
                break
    if len(FinalLRet) > len(lastSection):
        print(["".join(FinalLRet)])
    else:
        print(lret)
