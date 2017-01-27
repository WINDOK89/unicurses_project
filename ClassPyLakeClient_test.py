from unicurses import *
from PyLakeDriver import *

def color_init():
    init_pair(1, COLOR_WHITE, COLOR_BLACK)
    init_pair(2, COLOR_RED, COLOR_BLACK)
    init_pair(3, COLOR_BLUE, COLOR_BLACK)
    init_pair(4, COLOR_RED, COLOR_CYAN)
    init_pair(5, COLOR_YELLOW, COLOR_BLACK)

class PyLakeClient():
        
    def __init__(self):
        
        """intialization"""
        self.stdscr=initscr()
        
        """color init"""
        start_color()
        color_init()
        
        """allow special keey"""
        keypad(self.stdscr,True)
        
        """get max dim"""
        self.MaxX=getmaxyx(self.stdscr)[1]-1
        self.MaxY=getmaxyx(self.stdscr)[0]-1
        
        """init buffer and cmd"""
        self.Buffer=[]
        self.cmd=""
        
        """start loop"""
        while(self.cmd!="quit"):
            key=self.get_char(buf="".join(self.Buffer))
            self.manage_buffer(key)
                
        """terminate app"""
        endwin()

    def manage_buffer(self,key):
        
        """check if enter pressed"""
        if(key==10):
            self.cmd="".join(self.Buffer)
            self.Buffer=[]
            """manage cmd from here"""
            
        elif(key==263):    #check if backspace key pressed
            #check if len(buf) > 0 to avoid li[-1]
            if len(self.Buffer)>0:
                del self.Buffer[len(self.Buffer)-1]
            
        else:
            self.Buffer.append(chr(key))
            
        
        
        
    def get_char(self, message="Enter a command >> ", buf=""):
        
        """draw  separtion line between content and command"""
        move(self.MaxY-2,2)
        hline(ACS_HLINE,self.MaxX-2)
        move(self.MaxY,2)
        hline(ACS_HLINE,self.MaxX-2)
        move(1,2)
        hline(ACS_HLINE,self.MaxX-2)
        move(1,1)
        vline(ACS_VLINE,self.MaxY)
        move(1,self.MaxX-1)
        vline(ACS_VLINE,self.MaxY)
        
        """ask for the command"""
        attron(color_pair(2)+A_BOLD)
        mvaddstr(self.MaxY-1,3,message)
        attroff(color_pair(2)+A_BOLD)
        
        """add the buffer"""
        attron(color_pair(5)+A_BOLD)
        addstr(buf)
        
        """request character"""
        cmd=getch()
        attroff(color_pair(5)+A_BOLD)
        
        """clear full content"""
        clear()
        
        """return command"""
        return cmd
        
def main1():
	stdscr=initscr()
	move(2,3)
	co=getyx(stdscr)
	addstr("{}:{} {} ".format('set',co[0],co[1]))
	co=getparyx(stdscr)
	addstr("{}:{} {}".format('set',co[0],co[1]))
	window = newwin(10, 25, 0, 10)
	co=getyx(window)
	addstr("{}:{} {} ".format('set',co[0],co[1]))
	co=getparyx(window)
	addstr("{}:{} {}".format('set',co[0],co[1]))
	wmove(window,1,14)
	getch()
	endwin()
        
def main2():
	stdscr=initscr()
	keypad(stdscr,True)
	key=0
	noecho()
	cmd=""
	i=0
	lcmd=[]
	key=0
	while(cmd!="quit"):
		cmd="".join(lcmd)
		mvaddstr(1,i,str(key))
		i=i+7
		mvaddstr(2,0,cmd)
		move(0,0)
		key=getch()
		lcmd.append(chr(key))
		
		
		
	getch()
	endwin()

if __name__=="__main__":
    #a=PyLakeClient()
    main2()
