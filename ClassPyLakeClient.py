# -*- coding: utf-8 -*-
import ast
from unicurses import *
from PyLakeDriver import *
from ModuleStdTerminal import *
from ModulePyPowerCurveAgent import *
import matplotlib.pyplot as plt


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
        self.MyLake=PyLakeDriver("wintell", "wintell347", "148.251.51.21", DefaultDir="wintell/SR4/PCAgent")

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

        """keep going until the user enter quit"""
        while (self.cmd != "quit"):

            """retrieve a key from keyboard"""
            key = self.InputWindow.get_char(message=" {} # Terminal >> ".format(self.MyLake.DefaultDir), buf="".join(self.Buffer))

            """call overwritten manage_buffer"""
            self.manage_buffer(key)

            """to remove in the end, no reason to saty after finish"""
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
            """reinitialize the quit request flag, so we can have quit enter choice again after quiting once"""
            self.ChoiceWindow.quitRequest = True

            """get possibbility list only on the part before the cursor"""
            PosTag, lastSection = self.TagMemory.get_next(self.Buffer[:self.InputWindow.PosCur-len(self.InputWindow.message)])

            """if only 1, we display it in input window"""
            if len(PosTag) == 1:
                NewPositionCursor=len(self.InputWindow.message)+len(self.Buffer[:self.InputWindow.PosCur-len(self.InputWindow.message)] + list(PosTag[0])[len(lastSection):])
                self.Buffer = self.Buffer[:self.InputWindow.PosCur-len(self.InputWindow.message)] + list(PosTag[0])[len(lastSection):] + self.Buffer[self.InputWindow.PosCur-len(self.InputWindow.message):]
                self.InputWindow.PosCur = NewPositionCursor

                """if more than 1 we show the panel with everything possible"""
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
            """initialize the quit flag so we can use the menu again"""
            self.DirChoiceWindow.quitRequest = True

            """get possibbility list"""
            PosTag, lastSection = self.DirMemory.get_next(self.Buffer[:self.InputWindow.PosCur-len(self.InputWindow.message)])

            """if only 1, we display it in input window"""
            if len(PosTag) == 1:
                NewPositionCursor=len(self.InputWindow.message)+len(self.Buffer[:self.InputWindow.PosCur-len(self.InputWindow.message)] + list(PosTag[0])[len(lastSection):])
                self.Buffer = self.Buffer[:self.InputWindow.PosCur-len(self.InputWindow.message)] + list(PosTag[0])[len(lastSection):] + self.Buffer[self.InputWindow.PosCur-len(self.InputWindow.message):]
                self.InputWindow.PosCur = NewPositionCursor

                """if more than 1 we show the panel with everything possible"""
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

            """now we manage all the otehr possibility by caller the inherit fct which will do that for us"""
        else:
            StandardTerminal.manage_buffer(self,key)

    def cmd_manager(self):
        """
        The overwrttien fct will give all the reaction the program shell have on alll posiible commands
        :return:
        """
        cmdlist = self.cmd.split(" :")

        """help menu"""
        if cmdlist[0] == "help":
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("HELP CONTENT", color=2, attribute=A_BOLD + A_UNDERLINE)
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
            self.OutputWindow.add_text(
                "    --> '%p6' : tag directory, if none existing, it is created, it is optionnal ")
            self.OutputWindow.add_text("    --> Return: the new tag characteristics are returned")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'ssc :%p1 :%p2 :%p3':", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> change session credentials where: ")
            self.OutputWindow.add_text("    --> '%p1' : user name ")
            self.OutputWindow.add_text("    --> '%p2' : password ")
            self.OutputWindow.add_text("    --> '%p3' : DMLake Ip address ")
            self.OutputWindow.add_text("    --> Return: the new Url used is returned")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'av :%p1 :%p2 :%p3 :%p4':", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> add one value where: ")
            self.OutputWindow.add_text("    --> '%p1' : tag name ")
            self.OutputWindow.add_text("    --> '%p2' : time with format yyyy-mm-dd hh:mm:ss ")
            self.OutputWindow.add_text("    --> '%p3' : value ")
            self.OutputWindow.add_text("    --> '%p4' : optionnal directory ")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'avs :%p1 :%p2 :%p3':", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> add values where: ")
            self.OutputWindow.add_text("    --> '%p1' : tag name ")
            self.OutputWindow.add_text(
                "    --> '%p2' : list of list(time,value) with format [['2015-01-01 00:04:00',75],['2015-01-01 00:05:00',67]]")
            self.OutputWindow.add_text("    --> '%p3' : optionnal directory ")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'gv :%p1 :%p2 :%p3 :%p4'", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> get values ")
            self.OutputWindow.add_text("    --> '%p1' : tag name ")
            self.OutputWindow.add_text("    --> '%p2' : Start time, format: yyyy-mm-dd hh:mm:ss ")
            self.OutputWindow.add_text("    --> '%p3' : End time, format: yyyy-mm-dd hh:mm:ss ")
            self.OutputWindow.add_text("    --> '%p4' : optionnal directory where the tag is ")
            self.OutputWindow.add_text("    --> Return: list of time,value: [(t1,v1),(t2,v2),...]")
            self.OutputWindow.add_text(
                "    --> alternative: if '%p1' is given alone, it return the complete historian content for '%p1'")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'dts :%p1 :%p2'", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> delete tags")
            self.OutputWindow.add_text("    --> '%p1' : tag names list, format: ['tagname1','tagname2',...] ")
            self.OutputWindow.add_text("    --> '%p2' : optionnal directory where the tags are ")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'btd :%p1'", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> browse tag directory")
            self.OutputWindow.add_text("    --> '%p1' : optionnal directory where the tags are ")
            self.OutputWindow.add_text("    --> Return: list of tags displayed together with their metadatas")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'tt :%p1 :%p2 :%p3'", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> truncate tags")
            self.OutputWindow.add_text("    --> '%p1' : tag names list, format: ['tagname1','tagname2',...] ")
            self.OutputWindow.add_text(
                "    --> '%p2' : time from which all data must be deleted, format: yyyy-mm-dd hh:mm:ss")
            self.OutputWindow.add_text("    --> '%p3' : optionnal directory where the tags are ")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'gmd :%p1 :%p2'", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> get tag metadatas")
            self.OutputWindow.add_text("    --> '%p1' : tag name")
            self.OutputWindow.add_text("    --> '%p2' : optionnal directory where the tags are ")
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("cmd 'gmds :%p1 :%p2'", color=3, attribute=A_UNDERLINE)
            self.OutputWindow.add_text("")
            self.OutputWindow.add_text("    --> get tags metadatas")
            self.OutputWindow.add_text("    --> '%p1' : tag name list, format: ['tagname1','tagname2',...]")
            self.OutputWindow.add_text("    --> '%p2' : optionnal directory where the tags are ")

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "gd":  # get driectories
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("GET DIRECTORIES", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist) == 1:
                cmdlist.append("")
            """normally every cmd should be two comp"""
            if len(cmdlist) == 2:
                DirList = self.MyLake.get_tag_directories(TagDirParam="{}/{}".format("wintell", cmdlist[1]))
                if DirList != False:
                    self.OutputWindow.add_text("    --> wintell")
                    for elt in DirList:
                        finalStr = ""
                        eltSplit = elt.split('/')
                        for elt2 in eltSplit:
                            finalStr += "    "

                        self.OutputWindow.add_text("{}--> {}".format(finalStr, eltSplit[len(eltSplit) - 1]))
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "gtl":  # get tag list
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("GET TAG LIST", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist) == 1:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist) == 2:
                TagList = self.MyLake.get_tag_list(TagDirParam="{}".format(cmdlist[1]))
                if TagList != False:
                    self.OutputWindow.add_text("--> {}".format(self.MyLake.DefaultDir))
                    for elt in TagList:
                        finalStr = ""
                        eltSplit = elt.split('/')
                        for elt2 in eltSplit:
                            finalStr += "    "

                        self.OutputWindow.add_text("{}--> {}".format(finalStr, eltSplit[len(eltSplit) - 1]))
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "gv":  # get tag list
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("GET TAG VALUES", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """manage if just tag given"""
            if len(cmdlist) == 2:
                cmdlist.append("1970-01-01 01:00:00")
                cmdlist.append(get_utc_now(ReturnFormat="string"))
                cmdlist.append(self.MyLake.DefaultDir)

            """manage if user send no specific directory"""
            if len(cmdlist) == 4:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist) == 5:
                TagList = self.MyLake.get_values(cmdlist[1], cmdlist[2], cmdlist[3],
                                                 TagDirParam="{}".format(cmdlist[4]))
                if TagList != False:
                    self.OutputWindow.add_text("--> {}".format(self.MyLake.DefaultDir))
                    self.OutputWindow.add_text("    --> Get '{}'".format(cmdlist[1]))
                    self.OutputWindow.add_text("    --> from: {}".format(cmdlist[2]))
                    self.OutputWindow.add_text("    --> to: {}".format(cmdlist[3]))
                    self.OutputWindow.add_text("")
                    for elt in TagList:
                        self.OutputWindow.add_text("        {} || {}".format(utc_to_string(int(elt[0] / 1000)), elt[1]),
                                                   color=6, attribute=A_BOLD)
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "btd":  # get tag list
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("BROWSE TAG DIRECTORY", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist) == 1:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist) == 2:
                TagDict = self.MyLake.browse_directory(TagDirParam="{}".format(cmdlist[1]))
                if TagDict != False:
                    self.OutputWindow.add_text("--> {}".format(self.MyLake.DefaultDir))
                    for keyLevel1, eltLevel1 in TagDict.items():
                        keyLevel1Split = keyLevel1.split("/")
                        self.OutputWindow.add_text("    --> {}".format(keyLevel1Split[len(keyLevel1Split) - 1]))
                        for keyLevel2, eltLevel2 in eltLevel1.items():
                            self.OutputWindow.add_text("        --> {} : '{}'".format(keyLevel2, eltLevel2))
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "av":  # add value
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("ADD VALUE", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist) == 4:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist) == 5:
                self.OutputWindow.add_text("    --> Try  to insert in directory: {}".format(cmdlist[4]))
                self.OutputWindow.add_text("        --> Tag name: {}".format(cmdlist[1]))
                self.OutputWindow.add_text("        --> Time : {}".format(cmdlist[2]))
                self.OutputWindow.add_text("        --> Value: {}".format(cmdlist[3]))
                if self.MyLake.add_value(cmdlist[1], cmdlist[2], cmdlist[3], TagDirParam="{}".format(cmdlist[4])):
                    self.OutputWindow.add_text("    --> Successfully injected", color=6)
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "gmd":  # add value
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("GET TAG METADATAS", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist) == 2:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist) == 3:
                self.OutputWindow.add_text("    --> get metadatas in directory: {}".format(cmdlist[2]))
                self.OutputWindow.add_text("        --> Tag name: {}".format(cmdlist[1]))
                MData = self.MyLake.get_tag_metadata_get(cmdlist[1], TagDirParam=cmdlist[2])
                if MData != False:
                    for key, item in MData[0].items():
                        self.OutputWindow.add_text("            --> {}: {}".format(key, item), color=6)
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "avs":  # add value
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("ADD VALUES", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist) == 3:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist) == 4:
                self.OutputWindow.add_text("    --> Try  to insert in directory: {}".format(cmdlist[3]))
                self.OutputWindow.add_text("        --> Tag name: {}".format(cmdlist[1]))
                self.OutputWindow.add_text("        --> Values: {}".format(cmdlist[2]))
                ValuesList = string_to_list_tuple_dict(cmdlist[2])
                if ValuesList != False:
                    if self.MyLake.add_values(cmdlist[1], ValuesList, TagDirParam="{}".format(cmdlist[3])):
                        self.OutputWindow.add_text("    --> Successfully injected", color=6)
                    else:
                        self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!",
                                                   color=2)
                else:
                    self.OutputWindow.add_text("    !! LIST CONVERSION NOT POSSIBLE !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "dts":  # add value
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("DELETE TAGS", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist) == 2:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist) == 3:
                TagListToDelete = string_to_list_tuple_dict(cmdlist[1])
                if TagListToDelete != False:
                    self.OutputWindow.add_text("    --> Try to delete in directory: {}".format(cmdlist[2]))
                    self.OutputWindow.add_text("        --> Tag names: {}".format(cmdlist[1]))
                    if self.MyLake.delete_tags(TagListToDelete, TagDirParam=cmdlist[2]):
                        self.OutputWindow.add_text("    --> Successfully deleted", color=6)
                    else:
                        self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!",
                                                   color=2)

                else:
                    self.OutputWindow.add_text("    !! INPUT TAGLIST WRONG FORMAT !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "gmds":  # add value
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("GET TAGS METADATAS", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist) == 2:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist) == 3:
                TagListToGet = string_to_list_tuple_dict(cmdlist[1])
                if TagListToGet != False:
                    self.OutputWindow.add_text("    --> Try to Retrieve MetaDatas in directory: {}".format(cmdlist[2]))
                    self.OutputWindow.add_text("        --> Tag names: {}".format(cmdlist[1]))
                    MDatas = self.MyLake.get_tag_metadata_post(TagListToGet, TagDirParam=cmdlist[2])
                    if MDatas != False:
                        for elt in MDatas:
                            self.OutputWindow.add_text("")
                            for key, item in elt.items():
                                self.OutputWindow.add_text("            --> {}: {}".format(key, item), color=6)
                    else:
                        self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!",
                                                   color=2)

                else:
                    self.OutputWindow.add_text("    !! INPUT TAGLIST WRONG FORMAT !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "tt":  # truncate tags
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("TRUNCATE TAGS", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""
            """manage if user send no specific directory"""
            if len(cmdlist) == 3:
                cmdlist.append(self.MyLake.DefaultDir)
            """normally every cmd should be two comp"""
            if len(cmdlist) == 4:
                TagListToDelete = string_to_list_tuple_dict(cmdlist[1])
                if TagListToDelete != False:
                    self.OutputWindow.add_text("    --> Try to truncate in directory: {}".format(cmdlist[3]))
                    self.OutputWindow.add_text("        --> Tag names: {}".format(cmdlist[1]))
                    self.OutputWindow.add_text("        --> From: {}".format(cmdlist[2]))
                    if self.MyLake.truncate_tags(TagListToDelete, cmdlist[2], TagDirParam=cmdlist[3]):
                        self.OutputWindow.add_text("    --> Successfully truncated", color=6)
                    else:
                        self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!",
                                                   color=2)

                else:
                    self.OutputWindow.add_text("    !! INPUT TAGLIST WRONG FORMAT !!", color=2)

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "at":  # add tag
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("ADD TAG", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""

            """no default dir"""
            if len(cmdlist) == 6:
                cmdlist.append(self.MyLake.DefaultDir)

            """manage if user send no parameter"""
            if len(cmdlist) < 6:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            elif len(cmdlist) == 7:  # no default dir given
                TagList = self.MyLake.create_tags(cmdlist[1], TagType=cmdlist[2], TagUnit=cmdlist[3],
                                                  TagDescription=cmdlist[4], TagTitle=cmdlist[5],
                                                  TagDirParam="{}".format(cmdlist[6]))
                if TagList != False:
                    self.OutputWindow.add_text("    --> New tag '{}' in directory '{}'".format(cmdlist[1], cmdlist[6]))
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

            """to update tagmemory"""
            self.TagMemory = TagMemory(self.MyLake.browse_directory())

        elif cmdlist[0] == "sdd":  # set default directory
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("SET DEFAULT DIRECTORY", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""

            """normally every cmd should be two comp"""
            if len(cmdlist) == 2:
                self.OutputWindow.add_text("   --> Former directory: {}".format(self.MyLake.DefaultDir))
                self.MyLake.DefaultDir = cmdlist[1]
                self.OutputWindow.add_text("   --> new directory set: {}".format(self.MyLake.DefaultDir))

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

            """to update tagmemory"""
            self.TagMemory = TagMemory(self.MyLake.browse_directory())

        elif cmdlist[0] == "ssc":  # set default directory
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("SET SESSION CREDENTIALS", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """retrieve param"""

            """normally every cmd should be two comp"""
            if len(cmdlist) == 4:
                self.OutputWindow.add_text("   --> User name and password changed successfully")
                self.MyLake.Session.auth = (cmdlist[1], cmdlist[2])
                self.MyLake.UrlIp = "https://{}/tags/".format(cmdlist[3])
                self.OutputWindow.add_text("   --> new DMLake url set: {}".format(self.MyLake.UrlIp))

            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

        elif cmdlist[0] == "ad":  # add directory
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("ADD DIRECTORY", color=2, attribute=A_BOLD + A_UNDERLINE)
            self.OutputWindow.add_text("")

            """check parameter is there"""
            if len(cmdlist) == 2:
                if self.MyLake.create_directory(cmdlist[1]):
                    self.OutputWindow.add_text(
                        "    --> Directory '{}' has been created successfully".format(cmdlist[1]),
                        color=6)
                else:
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER !!", color=2)
            else:
                self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP2 !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True

            """to update tagmemory"""
            self.DirMemory = DirMemory(self.MyLake.get_tag_directories())

        elif cmdlist[0] == "plot":
            """plot power curve and model"""
            if len(cmdlist)==1:
                cmdlist.append(0.27998)
                cmdlist.append(0.3878)
                cmdlist.append(0.4604)
                cmdlist.append("2007-01-18 00:20:00")
                cmdlist.append("2017-01-31 00:00:00")

            if len(cmdlist)==6:
                powerList = self.MyLake.get_values("power", cmdlist[4], cmdlist[5])
                ylist = []

                SpeedList = self.MyLake.get_values("speed",cmdlist[4], cmdlist[5])
                xlist = []
                try:
                    for i, elt in enumerate(SpeedList):
                        if utc_to_string(powerList[i][0] / 1000) == utc_to_string(elt[0] / 1000):
                            ylist.append(powerList[i][1])
                            xlist.append(elt[1])
                        else:
                            pass
                except:
                    pass

                PowerModelList=[]
                for elt in xlist:
                    PowerModelList.append(get_power_model(elt, Omega=float(cmdlist[1]), Ksi=float(cmdlist[2]), AFactor=float(cmdlist[3])))

                #csv
                with open("export.csv",'a') as mf:
                    for i,elt in enumerate(xlist):
                        mf.write("{};{}\n".format(elt,ylist[i]))

                plt.ylabel("Power (Kw)")
                plt.xlabel("Wind Speed (m/s)")
                plt.grid()
                plt.axis([0,20,-20,2000])
                plt.plot(xlist, ylist, 'r.')
                plt.plot(xlist, PowerModelList, 'b.')
                plt.show()
            else:
                pass

        elif cmdlist[0] == "plotR":
            """plot residual"""
            if len(cmdlist)==1:
                cmdlist.append(0.27998)
                cmdlist.append(0.3878)
                cmdlist.append(0.4604)
                cmdlist.append("2007-01-18 00:20:00")
                cmdlist.append("2017-01-31 00:00:00")

            if len(cmdlist)==6:
                powerList = self.MyLake.get_values("power", cmdlist[4], cmdlist[5])
                ylist = []

                SpeedList = self.MyLake.get_values("speed",cmdlist[4], cmdlist[5])
                xlist = []
                try:
                    for i, elt in enumerate(SpeedList):
                        if utc_to_string(powerList[i][0] / 1000) == utc_to_string(elt[0] / 1000):
                            ylist.append(powerList[i][1])
                            xlist.append(elt[1])
                        else:
                            pass
                except:
                    pass

                PowerModelList=[]
                for elt in xlist:
                    PowerModelList.append(get_power_model(elt, Omega=float(cmdlist[1]), Ksi=float(cmdlist[2]), AFactor=float(cmdlist[3])))

                # #csv
                # with open("export.csv",'a') as mf:
                #     for i,elt in enumerate(xlist):
                #         mf.write("{};{}\n".format(elt,ylist[i]))

                ResList=get_residual(PowerModelList, ylist)

                plt.ylabel("Power (Kw)")
                plt.xlabel("Wind Speed (m/s)")
                plt.grid()
                #plt.axis([0,20,-20,2000])
                plt.plot(xlist, ResList, 'r.')
                plt.show()
            else:
                pass

        elif cmdlist[0] == "plotRR":
            """plot relevant residual"""
            if len(cmdlist) == 1:
                cmdlist.append(0.27998)
                cmdlist.append(0.3878)
                cmdlist.append(0.4604)
                cmdlist.append("2007-01-18 00:20:00")
                cmdlist.append("2017-01-31 00:00:00")

            if len(cmdlist) == 6:
                powerList = self.MyLake.get_values("power", cmdlist[4], cmdlist[5])
                ylist = []

                SpeedList = self.MyLake.get_values("speed", cmdlist[4], cmdlist[5])
                xlist = []
                try:
                    for i, elt in enumerate(SpeedList):
                        if utc_to_string(powerList[i][0] / 1000) == utc_to_string(elt[0] / 1000):
                            ylist.append(powerList[i][1])
                            xlist.append(elt[1])
                        else:
                            pass
                except:
                    pass

                PowerModelList = []
                for elt in xlist:
                    PowerModelList.append(
                        get_power_model(elt, Omega=float(cmdlist[1]), Ksi=float(cmdlist[2]), AFactor=float(cmdlist[3])))

                # #csv
                # with open("export.csv",'a') as mf:
                #     for i,elt in enumerate(xlist):
                #         mf.write("{};{}\n".format(elt,ylist[i]))

                ResList = get_residual(PowerModelList, ylist)
                ResListRelevant, VListRelevant = get_relevant_residual(ylist,ResList,xlist)

                plt.ylabel("Power (Kw)")
                plt.xlabel("Wind Speed (m/s)")
                plt.grid()
                # plt.axis([0,20,-20,2000])
                plt.plot(VListRelevant, ResListRelevant, 'r.')
                plt.show()
            else:
                pass

        elif cmdlist[0] == "plotRRD":
            """plot decision"""
            if len(cmdlist) == 1:
                cmdlist.append(0.27998)
                cmdlist.append(0.3878)
                cmdlist.append(0.4604)
                cmdlist.append("2007-01-18 00:20:00")
                cmdlist.append("2017-01-31 00:00:00")

            if len(cmdlist) == 6:
                powerList = self.MyLake.get_values("power", cmdlist[4], cmdlist[5])
                ylist = []

                SpeedList = self.MyLake.get_values("speed", cmdlist[4], cmdlist[5])
                xlist = []
                try:
                    for i, elt in enumerate(SpeedList):
                        if utc_to_string(powerList[i][0] / 1000) == utc_to_string(elt[0] / 1000):
                            ylist.append(powerList[i][1])
                            xlist.append(elt[1])
                        else:
                            pass
                except:
                    pass

                PowerModelList = []
                for elt in xlist:
                    PowerModelList.append(
                        get_power_model(elt, Omega=float(cmdlist[1]), Ksi=float(cmdlist[2]), AFactor=float(cmdlist[3])))

                # #csv
                # with open("export.csv",'a') as mf:
                #     for i,elt in enumerate(xlist):
                #         mf.write("{};{}\n".format(elt,ylist[i]))

                ResList = get_residual(PowerModelList, ylist)
                ResListRelevant, VListRelevant = get_relevant_residual(ylist,ResList,xlist)

                ResultList=[]
                for i in range(1,len(ResListRelevant)):
                    Dec=get_decision(ResListRelevant[:i])
                    ResultList.append(Dec)

                xlist=[]
                ylist=[]

                for i,elt in enumerate(ResultList):
                    xlist.append(i)
                    ylist.append(elt)

                plt.ylabel("Power (Kw)")
                plt.xlabel("Wind Speed (m/s)")
                plt.grid()
                # plt.axis([0,20,-20,2000])
                plt.plot(xlist, ylist, 'r.')
                plt.show()
            else:
                pass

        else:
            self.OutputWindow.clear_display()
            self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

            """to allow again the display object to run"""
            self.OutputWindow.quitRequest = True


def string_to_list_tuple_dict(s):
    """
    fct to convert string into dict, list, tuple
    :param s: the string to convert
    :return: false if error, the list,tuple,dicct if ok
    """
    try:
        ret=ast.literal_eval(s)
    except:
        return False
    else:
        return ret

if __name__ == "__main__":
    a=PyLakeClient()
