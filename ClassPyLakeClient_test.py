from ModuleStdTerminal import *

a=StandardTerminal()


def manage_buffer(self, key):
    """"""

    """to displlay at top display screen"""
    top_panel(self.OutputWindow.panel)
    bottom_panel(self.ChoiceWindow.panel)
    bottom_panel(self.DirChoiceWindow.panel)
    self.OutputWindow.show_changes()

    """copy buffer if we are not select memory"""
    if self.cmdEnterFlag:
        self.copyBuffer = self.Buffer
    self.cmdEnterFlag = True

    """check if enter pressed"""
    if (key == 10):
        self.cmd = "".join(self.Buffer)
        if self.cmd == "":
            pass
        else:
            self.cmdMemory.append(self.cmd)
        self.cmdMemoryIndex = 0
        self.Buffer = []
        self.InputWindow.PosCur = -1
        """manage cmd from here"""
        self.cmd_manager()

    elif (key == KEY_UP):

        if ((self.cmdMemoryIndex + 1) <= len(self.cmdMemory)) and (self.cmdMemoryIndex >= 0) and len(
                self.cmdMemory) != 0:
            self.cmdMemoryIndex += 1
            self.Buffer = list(self.cmdMemory[len(self.cmdMemory) - self.cmdMemoryIndex])
            self.InputWindow.PosCur = len(self.InputWindow.message) + len(self.Buffer)
        self.cmdEnterFlag = False

    elif (key == KEY_DOWN):

        if (self.cmdMemoryIndex >= 1) and ((self.cmdMemoryIndex - 1) < len(self.cmdMemory)) and len(
                self.cmdMemory) != 0:
            self.cmdMemoryIndex -= 1
            if self.cmdMemoryIndex == 0:
                self.Buffer = self.copyBuffer
                self.InputWindow.PosCur = len(self.InputWindow.message) + len(self.Buffer)
            else:
                self.Buffer = list(self.cmdMemory[len(self.cmdMemory) - self.cmdMemoryIndex])
                self.InputWindow.PosCur = len(self.InputWindow.message) + len(self.Buffer)
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
        self.Buffer.insert(self.InputWindow.PosCur - len(self.InputWindow.message), chr(key))
        self.InputWindow.PosCur += 1


def cmd_manager(self):
    """"""

    """get cmd list"""
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
        self.OutputWindow.add_text("    --> '%p6' : tag directory, if none existing, it is created, it is optionnal ")
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
            TagList = self.MyLake.get_values(cmdlist[1], cmdlist[2], cmdlist[3], TagDirParam="{}".format(cmdlist[4]))
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
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!", color=2)
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
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!", color=2)

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
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!", color=2)

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
                    self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER OR INPUT FORMAT WRONG !!", color=2)

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
                self.OutputWindow.add_text("    --> Directory '{}' has been created successfully".format(cmdlist[1]),
                                           color=6)
            else:
                self.OutputWindow.add_text("    !! CONNECTION ERROR WITH SERVER !!", color=2)
        else:
            self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP2 !!", color=2)

        """to allow again the display object to run"""
        self.OutputWindow.quitRequest = True

        """to update tagmemory"""
        self.DirMemory = DirMemory(self.MyLake.get_tag_directories())

    else:
        self.OutputWindow.clear_display()
        self.OutputWindow.add_text("    !! WRONG FORMAT, CONSULT HELP !!", color=2)

        """to allow again the display object to run"""
        self.OutputWindow.quitRequest = True

