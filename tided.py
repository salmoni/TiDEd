#!/usr/bin/env python2.3
#
# tided.py
# (c) 2009, Alan James Salmoni, Thought Into Design
# Tided - the text editor for OS X

import wxversion
wxversion.select('2.9')

import os
import os.path
import wx
import wx.stc as stc
import wx.aui
#import wx.lib.agw.buttonpanel as bp
import icons
import sys
import subprocess
import settings
import lang
import toolbar
import preferences

if wx.Platform == '__WXMSW__':
        faces = { 'times': 'Times New Roman',
                          'mono' : 'Courier New',
                          'helv' : 'Arial',
                          'other': 'Comic Sans MS',
                          'size' : 10,
                          'size2': 8,
                         }
elif wx.Platform == '__WXMAC__':
        faces = { 'times': 'Times New Roman',
                          'mono' : 'Monaco',
                          'helv' : 'Arial',
                          'other': 'Comic Sans MS',
                          'size' : 12,
                          'size2': 10,
                         }
else:
        faces = { 'times': 'Times',
                          'mono' : 'Courier',
                          'helv' : 'Helvetica',
                          'other': 'new century schoolbook',
                          'size' : 12,
                          'size2': 10,
                         }

languages = ['Plain text','Ada','Assembler','ASP','BAAN','Batch','Bullant','C++','Config (Apache)',
             'CSS','Diff','Eiffel','Fortran','HTML','SGML','VB Script','Javascript',
             'LaTeX','Lisp','Lua','Makefile','MatLab','NNCronTab','Pascal','Perl','PHP','POV',
             'Python','Ruby','Scriptol','SQL','TCL/Tk','Visual Basic','VBScript','XCode','XML']


class DropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    def OnDropFiles(self, x, y, files):
        print "dropping"
        for i in files:
            self.obj.parent.LoadFile(i)

class ResultsDisplay(stc.StyledTextCtrl):
    def __init__(self, parent, ID):
        stc.StyledTextCtrl.__init__(self, parent, ID)
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "fore:#000000,back:#FFFFFF,face:Courier,size:8")
        self.StyleSetSize(stc.STC_STYLE_DEFAULT, 11)
        self.SetUseHorizontalScrollBar(0)
        self.SetMarginLeft(0)
        self.SetMarginWidth(0, 0)
        self.SetMarginWidth(1, 5)
        self.StyleSetSize(4, 6)
        self.SetWrapMode(1)
        #sys.stderr = self
        #sys.stdout = self
        # only enable this for running code

    def write(self, outstring):
        self.AddText(outstring)

class PySTC(stc.StyledTextCtrl):
    def __init__(self, parent, ID, db):
        stc.StyledTextCtrl.__init__(self, parent, ID)
        fdt = DropTarget(self)
        self.SetDropTarget(fdt)
        self.SetSelBackground(1,"BLUE")
        self.SetSelForeground(1,"WHITE")
        #self.AutoCompShow(
        self.parent = parent
        self.empty = True
        self.db = db
        self.saved = False
        self.name = "Untitled"
        self.fline = self.db.GetPreference('lastPath', 'Str')
        self.MakeDefaults()
        self.changed = False
        self.language = ''
        self.langChoice = ''
        # need to read in config file
        # likely location is /Users/<name>/Library/Application Support/<tided/config.txt
        #self.CmdKeyAssign(90, wx.MOD_META, wx.stc.STC_CMD_UNDO)
        #self.CmdKeyAssign(90, wx.MOD_META|wx.MOD_SHIFT, wx.stc.STC_CMD_REDO)
        #self.CmdKeyAssign(88, wx.MOD_META, wx.stc.STC_CMD_CUT)
        #self.CmdKeyAssign(67, wx.MOD_META, wx.stc.STC_CMD_COPY)
        #self.CmdKeyAssign(86, wx.MOD_META, wx.stc.STC_CMD_PASTE)
        self.CmdKeyAssign(wx.stc.STC_KEY_LEFT, wx.stc.STC_SCMOD_ALT, wx.stc.STC_CMD_WORDLEFT)
        self.CmdKeyAssign(wx.stc.STC_KEY_RIGHT, wx.stc.STC_SCMOD_ALT, wx.stc.STC_CMD_WORDRIGHT)
        self.SetModEventMask(
                wx.stc.STC_MOD_INSERTTEXT|wx.stc.STC_MOD_DELETETEXT|wx.stc.STC_PERFORMED_UNDO|
                wx.stc.STC_PERFORMED_REDO
                )
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPressed)
        self.Bind(wx.stc.EVT_STC_CHANGE, self.ChangeMade)
        self.Bind(wx.stc.EVT_STC_DO_DROP, self.DropSomething)
        self.Bind(wx.stc.EVT_STC_SAVEPOINTREACHED, self.SavePointReached)
        self.Bind(wx.stc.EVT_STC_SAVEPOINTLEFT, self.SavePointLeft)

    def onKeyPressed(self, evt): 
        # test for control key press
        k = evt.GetKeyCode()
        if (evt.GetModifiers() == wx.MOD_META):
            # command pressed
            if (k == 314):
                self.HomeDisplay()
            elif (k == 316):
                self.LineEndDisplay()
            elif (k == 366): # page down
                self.parent.TabLeft()
            elif (k == 367): # page up
                self.parent.TabRight()
        elif (k == 344):
            # run the script!
            # this needs to be in a separate routine to use the parameters for each language
            if self.language != '':
                fn = self.fline + os.sep + self.name
                #print "running %s : (%s)"%(self.language, fn)
                out = self.parent.results
                ln = [self.language, fn]
                # fn =  # /Users/salmoni/Projects/TiDEd/index.html"]
                # res = subprocess.Popen(["open", "-a","/Applications/Safari.app", self.name]) # to start Safari with filename
                res = subprocess.Popen(ln, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                #res = subprocess.Popen(self.language + ' ' + fn).communicate()
                for i in res:
                    print i
            else:
                pass
                #print self.language
        elif (k == 345): # F6
            # test for panel
            #print dir(self.parent.search)
            self.parent.ShowInfoFrame()
        elif (k == 346): # F7
            self.ZoomIn()
        else:
            evt.Skip()
            self.ChangeMade(None)

    def ZoomIn(self):
        x = self.GetZoom()
        self.SetZoom(x + 1)

    def DropSomething(self, evt):
        self.SavePointLeft(evt)
        print dir(evt)
        print "Position = ",evt.Position
        print "Text = ",evt.DragText
        print "Result = ",evt.DragResult

    def SavePointReached(self, evt):
        wx.CallAfter(self.parent.nb.SetPageText, self.parent.nb.GetSelection(), self.name)
        if not self.saved:
            self.empty = True

    def SavePointLeft(self, evt):
        wx.CallAfter(self.parent.nb.SetPageText, self.parent.nb.GetSelection(), self.name+' *')
        self.empty = False

    def MakeDefaults(self):
        # temporary routine to set it up for Python defaults
        v = self.db.GetPreference('SetUseTabs', 'Boolean')
        self.SetUseTabs(v)
        v = self.db.GetPreference('SetIndentationGuides', 'Boolean')
        self.SetIndentationGuides(v)
        v = self.db.GetPreference('SetIndent', 'Int')
        self.SetIndent(v)
        v = self.db.GetPreference('SetViewEOL', 'Boolean')
        self.SetViewEOL(v)
        v = self.db.GetPreference('SetEOLMode', 'Int')
        self.SetEOLMode(v)
        v = self.db.GetPreference('SetBackSpaceUnIndents', 'Boolean')
        self.SetBackSpaceUnIndents(v)
        v = self.db.GetPreference('SetCaretForeground', 'String')
        self.SetCaretForeground(v)
        v = self.db.GetPreference('SetOvertype', 'Boolean')
        self.SetOvertype(v)
        v = self.db.GetPreference('SetScrollWidth', 'Int')
        self.SetScrollWidth(v)
        v = self.db.GetPreference('SetTabIndents', 'Boolean')
        self.SetTabIndents(v)
        v = self.db.GetPreference('SetTabWidth', 'Int')
        self.SetTabWidth(v)
        v = self.db.GetPreference('SetViewWhiteSpace', 'Int')
        self.SetViewWhiteSpace(v)
        v = self.db.GetPreference('SetWrapMode', 'Int')
        self.SetWrapMode(v)
        v = self.db.GetPreference('ViewHorizontalScrollBar', 'Boolean')
        self.SetUseHorizontalScrollBar(v)
        v = self.db.GetPreference('ViewVerticalScrollBar', 'Boolean')
        self.SetUseVerticalScrollBar(v)
        v = self.db.GetPreference('ViewLineNumbers', 'Boolean')
        if (v == False):
            self.SetMarginWidth(0, 0)
        else:
            self.SetMarginWidth(0, 10)
        v = self.db.GetPreference('ViewFolding', 'Boolean')
        if (v == False):
            self.SetMarginWidth(1, 0)
        else:
            self.SetMarginWidth(1, 15)
        self.SetMarginLeft(10)
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetProperty("fold", "1")
        #self.SetMarginWidth(0, 30)
        #self.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
        #self.SetMarginMask(1, stc.STC_MASK_FOLDERS)
        #self.SetMarginSensitive(1, True)
        #self.SetMarginWidth(1, 12)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")
        lang.SetAsPython(self)

    def getConfigs(self):
        # gets config data and returns the config name (cs) and value (vls)
        pass

    def ChangeMade(self, evt):
        t = self.GetLineCount()
        w = len(str(t)) * 10
        self.SetMarginWidth(0, w)

    def NewFileMethod(self):
        self.parent.Menu101(None)

    def OpenFileMethod(self):
        self.parent.Menu102(None)
        self.SetSavePoint()

    def CloseTabMethod(self):
        self.parent.Menu104(None)

    def SaveFileMethod(self):
        if (self.GetModify() == True):
            fn = self.fline + os.sep + self.name
            #try:
            self.SaveFile(fn)
            #except AttributeError:
                #self.SaveAsFileMethod()
            p = self.parent.nb.GetSelection()
            self.parent.nb.SetPageText(p, self.name)
            self.saved = True
            self.SetSavePoint()
            self.parent.mostRecentPath = self.fline
            self.parent.db.ChangeSetting('lastPath', self.parent.mostRecentPath)
            #except:
                #print "Error in plain saving"
        else:
            self.SaveAsFileMethod()

    def SaveAsFileMethod(self):
        dlg = wx.FileDialog(
            self, message="Save this file as...",
            defaultDir=self.fline,
            style=wx.SAVE | wx.FD_OVERWRITE_PROMPT
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPaths()
            name = os.path.split(self.path[0])[1]
            p = self.parent.nb.GetSelection()
            self.parent.names[p] = name
            self.name = name
            self.parent.nb.SetPageText(p, name)
            #try:
            self.SaveFile(self.path[0])
            self.saved = True
            self.SetSavePoint()
            self.parent.mostRecentPath = self.fline
            self.parent.db.ChangeSetting('lastPath', self.parent.mostRecentPath)
            if self.language == '':
                self.language = self.parent.SetLanguage(self)
            #except:
                #print "Error in saving as"

class InfoFrameClass(wx.MiniFrame):
    def __init__(self, parent, doc, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                    style=wx.DEFAULT_FRAME_STYLE):
        wx.MiniFrame.__init__(self, parent, -1, doc.name, pos=wx.DefaultPosition, 
                    size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE)
        self.CentreOnParent()
        self.SetTransparent(200)
        self.SetBackgroundColour(wx.BLACK)
        self.p = wx.Panel(self)
        self.p.SetBackgroundColour(wx.BLACK)
        wx.StaticText(self.p, -1, "Number of words : %s"%doc.GetLength(),
                        pos=(10,10)).SetForegroundColour(wx.WHITE)
        wx.StaticText(self.p, -1, "Number of lines : %s"%doc.GetLineCount(), 
                        pos=(10,30)).SetForegroundColour(wx.WHITE)
        wx.StaticText(self.p, -1, "Language     : %s"%doc.langChoice,
                        pos=(10,50)).SetForegroundColour(wx.WHITE)


class EdWin(wx.Frame):
    def __init__(self, parent, id, db):
        wx.Frame.__init__(self, parent, id, "Thought into Design")
        self.db = db
        cleanShutdown = self.db.ChangeSetting('cleanShutdown','False')
        
        if cleanShutdown == False:
            # go off and recover
            print "Recovery na"
        self.SetSizeHints(450, 300)
        self.SetMinSize((450,300))
        x = self.db.GetPreference('dlgXPos','Int')
        y = self.db.GetPreference('dlgYPos','Int')
        self.dlgPos = (x,y)
        x = self.db.GetPreference('width', 'Int')
        y = self.db.GetPreference('height', 'Int')
        self.SetClientSize((x,y)) # read from db along with next line for position
        x = self.db.GetPreference('xpos', 'Int')
        y = self.db.GetPreference('ypos', 'Int')
        self.SetPosition((x,y))
        self.Update()
        self.names = ["unnamed"]
        self.docs = []
        self.mostRecentPath = self.db.GetPreference('lastPath', 'Str')
        #self.tb = bp.ButtonPanel(self, -1, "")
        
        self.tb = self.CreateToolBar ( (wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT ) )
        self.tb.SetToolBitmapSize(( 32, 32 ))
        

        blank_img = icons.getblankBitmap()
        new_img = icons.getnew01Bitmap()
        open_img = icons.getopen01Bitmap()
        save_img = icons.getsave01Bitmap()
        #close_img = icons.getclose01Bitmap()

        self.Bind(wx.EVT_CLOSE, self.CloseThis)
        self.Bind(wx.EVT_FIND, self.OnFind)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFindNext)
        self.Bind(wx.EVT_FIND_REPLACE, self.OnReplace)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnReplaceAll)

        self.vs = wx.BoxSizer(wx.VERTICAL)
        self.hs = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.vs)

        self.search = wx.SearchCtrl(self.tb, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        self.search.Bind(wx.EVT_TEXT, self.OnIncrSearch)
        self.search.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        self.search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel)
        self.search.Bind(wx.EVT_KEY_DOWN, self.OnSearchKey)
        # self.search.SetDescriptiveText('replace')

        self.tb.AddLabelTool(1000, '', blank_img)
        self.tb.AddLabelTool(1001, 'New', new_img, longHelp='Begin a new document')
        #self.tb.AddLabelTool(1004, 'Close', close_img, longHelp="Close this tab")
        self.tb.AddLabelTool(1002, 'Open', open_img, longHelp='Open a new document')
        self.tb.AddLabelTool(1003, 'Save', save_img, longHelp='Save this document')
        self.tb.AddLabelTool(1000, '', blank_img)
        #self.tb.AddLabelTool(1004, 'Run', run_img)
        self.tb.AddLabelTool(1000, '', blank_img)
        self.tb.AddControl(self.search)
        self.tb.Realize()
        self.Bind(wx.EVT_TOOL, self.Menu101, id=1001)
        self.Bind(wx.EVT_TOOL, self.Menu102, id=1002)
        self.Bind(wx.EVT_TOOL, self.Menu105, id=1003)
        

        v = self.db.GetPreference('ViewStatusBar', 'String')
        self.CreateStatusBar() # switched off by default as is horizontal scrollbar
        self.sb = self.GetStatusBar()
        #self.sb.SetStatusWidths([-1, -1])

        self.splitter = wx.SplitterWindow(self, -1, style= wx.SP_LIVE_UPDATE)
        self.splitter.SetMinimumPaneSize(10)
        self.sashpos = 100
        self.splitter.SetSashSize(8)
        self.nb = wx.aui.AuiNotebook(self.splitter)
        self.prefsPanel = wx.Panel(self.nb, 888, (0,10), (10,10))
        # may need to create several tabs depending upon last position
        self.docs.append(PySTC(self, 0, self.db))
        self.nb.AddPage(self.docs[0], "Untitled") # use filename here
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.CloseTab, self.nb)
        self.m = wx.MenuBar()
        self.DragAcceptFiles(True)
        #self.vs.Add(self.nb, 1, wx.EXPAND)
        #self.results = PySTC(self.splitter, 0, self.db)
        self.results = ResultsDisplay(self.splitter, 1098)
        #sys.stderr = self.results
        self.splitter.SplitHorizontally(self.nb, self.results, -100)
        self.vs.Add(self.splitter, 1, wx.EXPAND)
        self.vs.Layout()

        self.m1a = wx.Menu()
        self.oldDocs = self.db.GetDocs()
        for i in range(len(self.oldDocs)):
            if i < 10:
                self.m1a.Append(1081+i, self.oldDocs[i])
        self.m1a.Append(1099, "Clear Menu")
        self.Bind(wx.EVT_MENU, self.ClearOldDocsMenu, id=1099)

        self.pd = wx.PrintData()
        self.pd.SetPaperId(wx.PAPER_A4)
        self.pd.SetPrintMode(wx.PRINT_MODE_PRINTER)

        self.m1b = wx.Menu()
        self.sessions = self.db.GetSessions()
        for i in range(len(self.sessions)):
            self.m1b.Append(1111+i, self.sessions[i])

        m1 = wx.Menu() # file
        m1.Append(101, '&New\tCtrl+N', "Begin a new document")
        m1.Append(102, "&Open\tCtrl+O", "Open an existing document")
        m1.AppendMenu(103, "Open recent", self.m1a) # need a list of files from the db
        m1.Append(104, "Close tab\tCtrl+W")
        m1.Append(113, "Close all tabs\tCtrl+Shift+W")
        m1.AppendSeparator()
        m1.AppendMenu(111, "Open session", self.m1b)
        m1.Append(112, "Save session", "Save this as a current session")
        m1.Append(113, "Manage sessions", "Edit or delete sessions")
        m1.AppendSeparator()
        m1.Append(105, "&Save\tCtrl+S", "Save this document now")
        m1.Append(106, "Save &As\tShift+Ctrl+S", "Save this document with a different name")
        m1.Append(111, "Save all\tShift+Ctrl+A", "Save all documents")
        m1.Append(107, "Export as")
        m1.Append(108, "Revert to saved")
        m1.AppendSeparator()
        m1.Append(109, "Print\tCtrl+P")
        m1.Append(110, "Page setup\tShift+Ctrl+P")
        self.Bind(wx.EVT_MENU, self.Menu101, id=101)
        self.Bind(wx.EVT_MENU, self.Menu102, id=102)
        self.Bind(wx.EVT_MENU, self.Menu104, id=104)
        self.Bind(wx.EVT_MENU, self.Menu105, id=105)
        self.Bind(wx.EVT_MENU, self.Menu106, id=106)
        self.Bind(wx.EVT_MENU, self.Menu109, id=109)
        self.Bind(wx.EVT_MENU, self.Menu110, id=110)
        self.Bind(wx.EVT_MENU, self.Menu111, id=111)
        self.Bind(wx.EVT_MENU, self.Menu112, id=112)
        self.Bind(wx.EVT_MENU, self.Menu113, id=113)
        self.Bind(wx.EVT_MENU_RANGE, self.SelectOldDocument, id=1081, id2=1091)
        self.Bind(wx.EVT_MENU_RANGE, self.LoadSession, id=1111, id2=1120)

        m2a = wx.Menu() # find submenu for edit menu
        m2a.Append(2081, "Find\tCtrl+F")
        m2a.Append(2082, "Find next\tCtrl+G")
        m2a.Append(2083, "Find previous\tShift+CTRL+G")
        m2a.Append(2084, "Find / Replace\tCtrl+R")

        m2b = wx.Menu() # Convert line endings
        m2b.Append(2091, "LF (Mac OS X, Unix, Linux)")
        m2b.Append(2092, "CR (Older Macintosh)")
        m2b.Append(2093, "CR/LF (Windows. DOS)")

        m2 = wx.Menu() # edit
        m2.Append(201, "Undo\tCtrl+Z")
        m2.Append(202, "Redo\tShift+Ctrl+Z")
        m2.AppendSeparator()
        m2.Append(203, "Cut\tCtrl+X")
        m2.Append(204, "Copy\tCtrl+C")
        m2.Append(205, "Paste\tCtrl+V")
        m2.Append(206, "Delete")
        m2.Append(207, "Select all\tCtrl+A")
        m2.AppendSeparator()
        m2.Append(211, "To lower case\tAlt+Ctrl+Shift+C")
        m2.Append(212, "To UPPER case\tCtrl+Shift+C")
        m2.AppendMenu(213, "Convert line endings to", m2b)
        m2.AppendSeparator()
        m2.AppendMenu(208, "Find", m2a)
        m2.AppendSeparator()
        m2.Append(209, "Spelling")
        m2.Append(210, "Special characters\tAlt+Ctrl+T")
        self.Bind(wx.EVT_MENU, self.Menu201, id=201)
        self.Bind(wx.EVT_MENU, self.Menu202, id=202)
        self.Bind(wx.EVT_MENU, self.Menu203, id=203)
        self.Bind(wx.EVT_MENU, self.Menu204, id=204)
        self.Bind(wx.EVT_MENU, self.Menu205, id=205)
        self.Bind(wx.EVT_MENU, self.Menu206, id=206)
        self.Bind(wx.EVT_MENU, self.Menu207, id=207)
        self.Bind(wx.EVT_MENU, self.Menu211, id=211)
        self.Bind(wx.EVT_MENU, self.Menu212, id=212)
        self.Bind(wx.EVT_MENU, self.Menu2091, id=2091)
        self.Bind(wx.EVT_MENU, self.Menu2092, id=2092)
        self.Bind(wx.EVT_MENU, self.Menu2093, id=2093)
        self.Bind(wx.EVT_MENU, self.Menu2081, id=2081)
        self.Bind(wx.EVT_MENU, self.Menu2082, id=2082)
        self.Bind(wx.EVT_MENU, self.Menu2083, id=2083)
        self.Bind(wx.EVT_MENU, self.Menu2084, id=2084)

        m3 = wx.Menu() # format
        m3.Append(301, "Text font")
        m3.Append(302, "Background colour")
        m3.Append(303, "blah")

        m6a = wx.Menu() # languages submenu for programming menu
        la = len(languages)
        for i in range(la):
            m6a.Append(1601 + i, languages[i], "", wx.ITEM_RADIO)
        m6 = wx.Menu() # programming
        m6.Append(601, "Run/Compile\tF5")
        m6.Append(602, "Run/compile options\tShift+F5")
        m6.AppendMenu(603, "Change language", m6a)
        self.Bind(wx.EVT_MENU_RANGE, self.ChangeLanguage, id=1601, id2=1700)

        m4c = wx.Menu() # show white space
        m4c.Append(4091, "never")
        m4c.Append(4092, "only after indent")
        m4c.Append(4093, "always")

        m4 = wx.Menu() # View
        m4.Append(401, "Tool bar", "", wx.ITEM_CHECK)
        #m4.Append(402, "Tabs", "", wx.ITEM_CHECK)
        m4.Append(403, "Status bar", "", wx.ITEM_CHECK)
        m4.Append(404, "Horizontal scrollbar", "", wx.ITEM_CHECK)
        m4.Append(405, "Vertical scrollbar", "", wx.ITEM_CHECK)
        m4.Append(406, "Line numbers", "", wx.ITEM_CHECK)
        m4.Append(407, "Folding", "", wx.ITEM_CHECK)
        m4.Append(408, "Word wrap","",wx.ITEM_CHECK)
        m4.Append(414, "Hide 'output'","",wx.ITEM_CHECK)
        m4.Append(409, "Wrap 'output'","",wx.ITEM_CHECK)
        m4.Append(410, "Indentation guides","",wx.ITEM_CHECK)
        m4.Append(413, "Use monospaced font", "",wx.ITEM_CHECK)
        m4.Append(411, "EOL Characters","",wx.ITEM_CHECK)
        m4.AppendMenu(412, "Show white space", m4c)
        doc = self.docs[0]

        val = self.db.GetPreference('ViewToolBar','Boolean')
        if val:
            m4.Check(401, True)
        else:
            m4.Check(401, False)

        val = self.db.GetPreference('ViewStatusBar','Boolean')
        if val:
            m4.Check(403, True)
        else:
            m4.Check(403, False)

        val = self.db.GetPreference('ViewHorizontalScrollBar','Boolean')
        if val:
            m4.Check(404, True)
        else:
            m4.Check(404, False)

        val = self.db.GetPreference('ViewVerticalScrollBar','Boolean')
        if val:
            m4.Check(405, True)
        else:
            m4.Check(405, False)

        val = self.db.GetPreference('ViewLineNumbers','Boolean')
        if val:
            m4.Check(406, True)
        else:
            m4.Check(406, False)

        val = self.db.GetPreference('ViewFolding','Boolean')
        if val:
            m4.Check(407, True)
        else:
            m4.Check(407, False)

        v = self.db.GetPreference('SetWrapMode', 'Boolean')
        if v:
            m4.Check(408, True)
        else:
            m4.Check(408, False)
        v = self.results.GetWrapMode()
        m4.Check(409, -v)
        self.results.SetWrapMode(v)
        self.results.SetUseHorizontalScrollBar(-v)
        val = self.db.GetPreference('SetIndentationGuides','Boolean')
        if val:
            m4.Check(410, True)
        else:
            m4.Check(410, False)
        val = self.db.GetPreference('SetViewEOL','Boolean')
        if val:
            m4.Check(411, True)
        else:
            m4.Check(411, False)

        self.Bind(wx.EVT_MENU, self.Menu401, id=401)
        self.Bind(wx.EVT_MENU, self.Menu403, id=403)
        self.Bind(wx.EVT_MENU, self.Menu404, id=404)
        self.Bind(wx.EVT_MENU, self.Menu405, id=405)
        self.Bind(wx.EVT_MENU, self.Menu406, id=406)
        self.Bind(wx.EVT_MENU, self.Menu407, id=407)
        self.Bind(wx.EVT_MENU, self.Menu408, id=408)
        self.Bind(wx.EVT_MENU, self.Menu409, id=409)
        self.Bind(wx.EVT_MENU, self.Menu410, id=410)
        self.Bind(wx.EVT_MENU, self.Menu411, id=411)
        self.Bind(wx.EVT_MENU, self.Menu414, id=414)
        self.Bind(wx.EVT_MENU, self.Menu4091, id=4091)
        self.Bind(wx.EVT_MENU, self.Menu4092, id=4092)
        self.Bind(wx.EVT_MENU, self.Menu4093, id=4093)

        m5 = wx.Menu() # bookmarks
        m5.Append(501, "Add bookmark for here")
        m5.Append(502, "Manage all bookmarks")
        m5.Append(503, "bookmark #1")

        m7 = wx.Menu()
        #item = m7.Append(wx.ID_EXIT, text="&Quit")
        #self.Bind(wx.ID_EXIT, self.CloseApp, -1)
        item = m7.Append(wx.ID_HELP, "Test & Help", "Help information")
        self.Bind(wx.EVT_MENU, self.OnHelp, item)
        item = m7.Append(wx.ID_ABOUT, "&About TiDEd", "More information about TiDEd")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        item = m7.Append(wx.ID_PREFERENCES, text="&Preferences\tCtrl+,")
        self.Bind(wx.EVT_MENU, self.OnPrefs, item)
        #item = m7.Append(wx.ID_QUIT, "&Quit\tCmd+Q")

        self.m.Append(m1, "&File")
        self.m.Append(m2, "Edit")
        self.m.Append(m3, "Format")
        self.m.Append(m6, "Programming")
        self.m.Append(m4, "View")
        self.m.Append(m5, "Bookmarks")
        self.m.Append(m7, "&Help")
        self.SetMenuBar(self.m)
        v = self.db.GetPreference('ViewStatusBar', 'Boolean')
        sb = self.GetStatusBar()
        if (v == True):
            sb.Show(True)
        else:
            sb.Hide()
        v = self.db.GetPreference('ViewToolBar', 'Boolean')
        if (v == True):
            self.tb.Show(True)
        else:
            self.tb.Show(False)

    def ShowInfoFrame(self):
        p = self.nb.GetSelection()
        doc = self.docs[p]
        infoWin = InfoFrameClass(self, doc)
        infoWin.Show(True)

    def TabFocus(self, evt):
        print "has focus"

    def OnIncrSearch(self, evt, sstr=None):
        # check if a selection is made - if so, search only in there
        self.search.SetForegroundColour("BLACK")
        if sstr == None:
            sstr = self.search.GetValue()
        l = len(sstr)
        p = self.nb.GetSelection()
        doc = self.docs[p]
        if (l == 1):
            # first go - record the position
            self.lastpos = doc.GetCurrentPos()
        fpos = 0
        lpos = doc.GetLength()
        self.pos = doc.FindText(fpos, lpos, sstr)
        if (self.pos == -1):
            # nothing found
            # need a visual signal for this
            self.search.SetForegroundColour("RED")
            pass
        else:
            doc.SetSelection(self.pos, self.pos + l)

    def OnSearch(self, evt):
        self.search.SetForegroundColour("BLACK")
        p = self.nb.GetSelection()
        self.docs[p].SetFocus()

    def OnCancel(self, evt):
        # cancel the search
        self.search.SetValue('')
        p = self.nb.GetSelection()
        self.docs[p].SetFocus()
        try:
            self.docs[p].GotoPos(self.lastpos)
        except AttributeError:
            pass

    def OnSearchKey(self, evt):
        k = evt.GetKeyCode()
        m = evt.GetModifiers()
        #if (evt.GetModifiers() == wx.MOD_META):
        if (k == 27):
            if self.search.GetValue() == '':
                p = self.nb.GetSelection()
                self.docs[p].SetFocus()
            else:
                self.OnCancel(evt)
        elif (k == 9):
            if (m == 0):
                self.SearchForward(evt)
            elif (m == 4):
                self.SearchBackward(evt)
        else:
            evt.Skip()

    def SearchForward(self, evt, sstr=None):
        p = self.nb.GetSelection()
        if sstr == None:
            sstr = self.search.GetValue()
        doc = self.docs[p]
        lpos = doc.GetLength()
        try:
            self.pos = doc.FindText(self.pos + 1, lpos, sstr)
        except:
            self.pos = 0
        if self.pos != -1:
            doc.SetSelection(self.pos, self.pos + len(sstr))
            self.search.SetForegroundColour("BLACK")
            doc.SearchAnchor()
        else:
            self.pos = 0
            #print dir(self.search)
            self.search.SetForegroundColour("BLUE")
            self.search.SetBackgroundColour("BLACK")

    def SearchBackward(self, evt):
        p = self.nb.GetSelection()
        sstr = self.search.GetValue()
        doc = self.docs[p]
        lpos = doc.GetLength()
        self.pos = doc.SearchPrev(-1, sstr)
        if self.pos == -1:
            self.pos = doc.FindText(lpos, 0, sstr, 0)
            doc.SearchAnchor()
            doc.GotoPos(self.pos)
            doc.SetSelection(self.pos, self.pos+len(sstr))
            self.search.SetForegroundColour("BLUE")
        else:
            doc.SearchAnchor()
            doc.GotoPos(self.pos)
            doc.SetSelection(self.pos, self.pos+len(sstr))
            self.search.SetForegroundColour("BLACK")

    def Menu101(self, evt):
        #add new tab
        self.names.append("")
        self.docs.append(PySTC(self, -1, self.db))
        l = len(self.docs) - 1
        self.nb.AddPage(self.docs[l], "untitled")
        self.nb.SetSelection(l)
        self.docs[l].SetSTCFocus(True)

    def Menu102(self, evt):
        # open a file
        dlg = wx.FileDialog(
            self, message="Open a file",
            defaultDir=self.mostRecentPath,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST
            )
        if dlg.ShowModal() == wx.ID_OK:
            p = dlg.GetPaths()
            for i in p:
                self.LoadFile(i)

    def LoadFile(self, filename):
        fline, fname = os.path.split(filename)
        p = self.nb.GetSelection()
        doc = self.docs[p]
        usedFlag = False
        for i in range(len(self.docs)):
            if (fline == self.docs[i].fline) and (fname == self.docs[i].name):
                usedFlag = True
                tab = i
        if usedFlag:
            self.nb.SetSelection(tab)
        else:
            if not doc.empty:
                self.Menu101(None)
                p = self.nb.GetSelection()
                doc = self.docs[p]
                doc.path = filename
            # load file in self.path
            #doc.fline, doc.name = os.path.split(doc.path[0])
            doc.fline = fline
            doc.name = fname
            doc.LoadFile(filename)
            doc.ext = os.path.splitext(fname)[1]
            doc.language = self.SetLanguage(doc)
            self.nb.SetPageText(p, fname)
            # now add to db
            self.db.AddFile(filename)
            doc.empty = False
            doc.saved = True
            doc.SetSavePoint()
            self.mostRecentPath = doc.fline
            self.db.ChangeSetting('lastPath', self.mostRecentPath)

    def SetLanguage(self, doc):
        e = doc.ext
        e == e.lower()
        if e == '.py' or e == '.pyw':
            l = lang.SetAsPython(doc)
        elif e == '.ads' or e == '.adb':
            l = lang.SetAsAda(doc)
        elif e == '.html' or e == '.htm' or e == '.php' or e == '.shtml' or e == '.xhtml' or e == '.dhtml' or e == '.php3':
            l = lang.SetAsHTML(doc)
        elif e == '.asp':
            l = lang.SetAsASP(doc)
        elif e == '.c' or e == '.cc' or e == '.cpp' or e == '.cxx' or e == '.h' or e == '.hh' or e == '.hpp' or e == '.hxx':
            l = lang.SetAsCPP(doc)
        elif e == '.tex' or e == '.latex' or e == '.lyx':
            l = lang.SetAsLatex(doc)
        elif e == '.lsp' or e == '.lisp':
            l = lang.SetAsLisp(doc)
        elif e == '.asm':
            l = lang.SetAsASM(doc)
        elif e == '.f' or e == '.f77' or e == '.for' or e == '.f90':
            l = lang.SetAsFortran(doc)
        elif e == '.css':
            l = lang.SetAsCSS(doc)
        elif e == '.vb' or e == '.bas':
            l = lang.SetAsVisualBasic(doc)
        elif e == '.m' or e == '.mat' or e == '.mex' or e == '.mx' or e == '.mx3':
            l = lang.SetAsMatlab(doc)
        elif e == '.make':
            l = lang.SetAsMake(doc)
        elif e == '.e':
            l = lang.SetAsEiffel(doc)
        elif e == '.diff':
            l = lang.SetAsDiff(doc)
        elif e == '.conf':
            l = lang.SetAsConf(doc)
        elif e == '.bat':
            l = lang.SetAsBatch(doc)
        elif e == '.tcl' or e == '.tk':
            l = lang.SetAsTCL(doc)
        elif e == '.rb' or e == '.rbx' or e == '.rhtml' or e == '.ruby':
            l = lang.SetAsRuby(doc)
        elif e == '.sql':
            l = lang.SetAsSQL(doc)
        else:
            l = ''
        return l

    def CloseTab(self, evt):
        l = self.nb.GetPageCount()
        #p = self.nb.Get
        if (l <= 1):
            evt.Veto()
        else:
            p = self.nb.GetSelection()
            if self.docs[p].GetModify():
                # prompt to save first
                dlg = wx.MessageDialog(self, "This file is not saved! Do you want to save it now?",
                                       "Unsaved file", style=wx.YES_NO | wx.CANCEL | wx.ICON_EXCLAMATION)
                rtnval = dlg.ShowModal()
                if (rtnval == wx.ID_YES):
                    # check if it has a name first
                    if self.doc[p].name == "Untitled":
                        # has no name
                        self.docs[p].SaveAsFileMethod()
                        self.names.pop(p)
                        self.docs.pop(p)
                    else:
                        self.docs[p].SaveFileMethod()
                        self.names.pop(p)
                        self.docs.pop(p)
                elif (rtnval == wx.ID_NO):
                    self.names.pop(p)
                    self.docs.pop(p)
                    #self.nb.DeletePage(p)
                else:
                    evt.Veto()
            else:
                self.names.pop(p)
                self.docs.pop(p)
                #self.nb.DeletePage(p)

    def Menu104(self, evt):
        # close tab
        l = len(self.docs)
        if (l > 1):
            # check doc has been saved first
            p = self.nb.GetSelection()
            if self.docs[p].GetModify():
                # prompt to save first
                dlg = wx.MessageDialog(self, "This file is not saved! Do you want to save it now?",
                                       "Unsaved file", style=wx.YES_NO | wx.CANCEL | 
                                       wx.ICON_EXCLAMATION | wx.FD_OVERWRITE_PROMPT )
                rtnval = dlg.ShowModal()
                if (rtnval == wx.ID_YES):
                    # check if it has a name first
                    if self.names[p] == "Untitled":
                        # has no name
                        self.docs[p].SaveAsFileMethod()
                        self.names.pop(p)
                        self.docs.pop(p)
                        self.nb.DeletePage(p)
                    else:
                        self.docs[p].SaveFileMethod()
                        self.names.pop(p)
                        self.docs.pop(p)
                        self.nb.DeletePage(p)
                elif (rtnval == wx.ID_NO):
                    self.names.pop(p)
                    self.docs.pop(p)
                    self.nb.DeletePage(p)
                else:
                    evt.Veto()
            else:
                self.names.pop(p)
                self.docs.pop(p)
                self.nb.DeletePage(p)

    def Menu105(self, evt):
        p = self.nb.GetSelection()
        self.docs[p].SaveFileMethod()

    def Menu106(self, evt):
        p = self.nb.GetSelection()
        self.docs[p].SaveAsFileMethod()

    def Menu109(self, evt):
        p = self.nb.GetSelection()
        # self.docs[p].
        print "printing"
        pdd = wx.PrintDialogData(self.pd)
        printer = wx.Printer(pdd)
        ToBePrinted = self.docs[p]
        self.pd = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
        ToBePrinted.Destroy()

    def Menu110(self, evt):
        p = self.nb.GetSelection()
        # self.docs[p].
        psdd = wx.PageSetupDialogData(self.pd)
        psdd.CalculatePaperSizeFromId()
        dlg = wx.PageSetupDialog(self, psdd)
        dlg.ShowModal()
        self.pd = wx.PrintData( dlg.GetPageSetupData().GetPrintData() )
        dlg.Destroy()

    def Menu111(self, evt):
        for i in self.docs:
            if i.GetModify():
                if i.name == "untitled": # this needs to change as in Menu113
                    i.SaveAsFileMethod()
                else:
                    i.SaveFileMethod()

    def Menu112(self, evt):
        self.db.SaveSession(self)

    def Menu113(self, evt):
        print "closing all"
        self.Menu101(None)
        for i in range(len(self.docs)-2, -1, -1): # go through in reverse
            print "closing ",i
            doc = self.docs[i]
            if doc.GetModify():
                self.nb.SetSelection(i)
                dlg = wx.MessageDialog(self, "This file is not saved! Do you want to save it now?",
                                       "Unsaved file", style=wx.YES_NO | wx.CANCEL | wx.ICON_EXCLAMATION)
                rtnval = dlg.ShowModal()
                if (rtnval == wx.ID_YES):
                    # check if it has a name first
                    if doc.name == "untitled":
                        # has no name
                        doc.SaveAsFileMethod()
                        self.names.pop(i)
                        self.docs.pop(i)
                    else:
                        doc.SaveFileMethod()
                        self.names.pop(i)
                        self.docs.pop(i)
                elif (rtnval == wx.ID_NO):
                    self.names.pop(i)
                    self.docs.pop(i)
                    self.nb.DeletePage(i)
                else:
                    evt.Veto()
            else:
                self.names.pop(i)
                self.docs.pop(i)
                self.nb.DeletePage(i)

    def Menu201(self, evt):
        # undo action
        p = self.nb.GetSelection()
        self.docs[p].Undo()

    def Menu202(self, evt):
        # redo action
        p = self.nb.GetSelection()
        self.docs[p].Redo()

    def Menu203(self, evt):
        # cut to clipboard
        p = self.nb.GetSelection()
        self.docs[p].Cut()

    def Menu204(self, evt):
        # copy to clipboard
        p = self.nb.GetSelection()
        self.docs[p].Copy()

    def Menu205(self, evt):
        # paste to clipboard
        p = self.nb.GetSelection()
        if self.docs[p].CanPaste():
            self.docs[p].Paste()

    def Menu206(self, evt):
        # delete selection or character
        p = self.nb.GetSelection()
        self.docs[p].DeleteBack()

    def Menu207(self, evt):
        # select all
        p = self.nb.GetSelection()
        self.docs[p].SelectAll()

    def Menu211(self, evt):
        # convert to lower case
        p = self.nb.GetSelection()
        self.docs[p].LowerCase()

    def Menu212(self, evt):
        # convert to UPPER case
        p = self.nb.GetSelection()
        self.docs[p].UpperCase()

    def Menu2081(self, evt):
        self.search.SetFocus()

    def Menu2082(self, evt):
        self.SearchForward(evt)

    def Menu2083(self, evt):
        self.SearchBackward(evt)

    def Menu2084(self, evt):
        sstr = self.search.GetValue()
        # find / replace
        data = wx.FindReplaceData()
        if sstr != '':
            data.SetFindString(sstr)
        dlg = wx.FindReplaceDialog(self, data, "Find & Replace", wx.FR_REPLACEDIALOG)
        dlg.data = data
        dlg.Show(True)

    def OnFind(self, evt):
        self.OnIncrSearch(evt, evt.GetFindString())

    def OnFindNext(self, evt):
        self.SearchForward(evt, evt.GetFindString())

    def OnReplace(self, evt):
        print "Find: %s, Replace: %s"%(evt.GetFindString(), evt.GetReplaceString())
        self.OnFindNext(evt)
        print self.pos

    def OnReplaceAll(self, evt):
        print "Find all: %s, Replace: %s"%(evt.GetFindString(), evt.GetReplaceString())

    def Menu2091(self, evt):
        p = self.nb.GetSelection()
        self.docs[p].ConvertEOLs(wx.stc.STC_EOL_LF)

    def Menu2092(self, evt):
        p = self.nb.GetSelection()
        self.docs[p].ConvertEOLs(wx.stc.STC_EOL_CR)

    def Menu2093(self, evt):
        p = self.nb.GetSelection()
        self.docs[p].ConvertEOLs(wx.stc.STC_EOL_CRLF)

    def Menu401(self, evt):
        val = self.db.GetPreference('ViewToolBar','Boolean')
        if val:
            self.tb.Show(False)
            self.vs.Layout()
            self.db.ChangeSetting('ViewToolBar', '0')
            # change database (hide toolbar)
        else:
            self.tb.Show(True)
            self.vs.Layout()
            self.db.ChangeSetting('ViewToolBar', '1')
            # change database (show toolbar)

    def Menu403(self, evt):
        val = self.db.GetPreference('ViewStatusBar','Boolean')
        sb = self.GetStatusBar()
        if val:
            sb.Hide()
            e = wx.SizeEvent(self.GetSize())
            self.GetEventHandler().ProcessEvent(e)
            # change database (hide statusbar)
            self.db.ChangeSetting('ViewStatusBar', '0')
        else:
            sb.Show(True)
            e = wx.SizeEvent(self.GetSize())
            self.GetEventHandler().ProcessEvent(e)
            # change database (show statusbar)
            self.db.ChangeSetting('ViewStatusBar', '1')

    def Menu404(self, evt):
        val = self.db.GetPreference('ViewHorizontalScrollBar','Boolean')
        if val:
            for i in self.docs:
                i.SetUseHorizontalScrollBar(0)
            # change database (hide H scrollbar)
            self.db.ChangeSetting('ViewHorizontalScrollBar', '0')
        else:
            for i in self.docs:
                i.SetUseHorizontalScrollBar(True)
            # change database (show H scrollbar)
            self.db.ChangeSetting('ViewHorizontalScrollBar', '1')

    def Menu405(self, evt):
        val = self.db.GetPreference('ViewVerticalScrollBar','Boolean')
        if val:
            for i in self.docs:
                i.SetUseVerticalScrollBar(False)
            # change database (hide V scrollbar)
            self.db.ChangeSetting('ViewVerticalScrollBar', '0')
        else:
            for i in self.docs:
                i.SetUseVerticalScrollBar(True)
            # change database (show V scrollbar)
            self.db.ChangeSetting('ViewVerticalScrollBar', '1')

    def Menu406(self, evt):
        w = self.docs[0].GetMarginWidth(0)
        if w == 0:
            w = 25
            t = '1'
        else:
            w = 0
            t = '0'
        for i in self.docs:
            i.SetMarginWidth(0, w)
        self.db.ChangeSetting('ViewLineNumbers',t)

    def Menu407(self, evt):
        w = self.docs[0].GetMarginWidth(1)
        if w == 0:
            w = 15
            t = '1'
        else:
            w = 0
            t = '0'
        for i in self.docs:
            i.SetMarginWidth(1, w)
        self.db.ChangeSetting('ViewFolding', t)

    def Menu408(self, evt):
        p = self.nb.GetSelection()
        ch = evt.IsChecked()
        self.docs[p].SetWrapMode(ch)

    def Menu409(self, evt):
        ch = evt.IsChecked()
        self.results.SetWrapMode(ch)
        if ch == True:
            self.results.SetUseHorizontalScrollBar(False)
        else:
            self.results.SetUseHorizontalScrollBar(True)

    def Menu410(self, evt):
        # view indentation guides
        val = self.db.GetPreference('SetIndentationGuides','Boolean')
        if val == True:
            val = False
        else:
            val = True
        for i in self.docs:
            i.SetIndentationGuides(val)
        self.db.ChangeSetting('SetIndentationGuides',str(val))

    def Menu411(self, evt):
        # view EOL chars
        val = self.db.GetPreference('SetViewEOL','Boolean')
        if val == True:
            val = False
        else:
            val = True
        for i in self.docs:
            i.SetViewEOL(val)
        self.db.ChangeSetting('SetViewEOL',str(val))

    def Menu414(self, evt):
        p = self.splitter.GetSashPosition()
        if p < 11:
            self.splitter.SetSashPosition(100)
        else:
            self.splitter.SetSashPosition(10)

    def Menu4091(self, evt):
        for i in self.docs:
            i.SetViewWhiteSpace(wx.stc.STC_WS_INVISIBLE)
        self.db.ChangeSetting('SetViewWhiteSpace','0')

    def Menu4092(self, evt):
        for i in self.docs:
            i.SetViewWhiteSpace(wx.stc.STC_WS_VISIBLEAFTERINDENT)
        self.db.ChangeSetting('SetViewWhiteSpace','2')

    def Menu4093(self, evt):
        for i in self.docs:
            i.SetViewWhiteSpace(wx.stc.STC_WS_VISIBLEALWAYS)
        self.db.ChangeSetting('SetViewWhiteSpace','1')

    def TabLeft(self):
        p = self.nb.GetSelection()
        t = self.nb.GetPageCount()
        p = p - 1
        if p < 0:
            p = t - 1
        print 'p = ',p
        self.nb.SetSelection(p)

    def TabRight(self):
        p = self.nb.GetSelection()
        t = self.nb.GetPageCount()
        p = p + 1
        if p > t - 1:
            p = 0
        print 'p = ',p
        self.nb.SetSelection(p)

    def OnHelp(self, evt):
        dlg = wx.MessageDialog(self, "Help here\n" "line 2", "line 3", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnAbout(self, evt):
        dlg = wx.MessageDialog(self, "the OS X Programmer's Editor"
                               ,"TiDEd",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPrefs(self, evt):
        p = self.nb.GetSelection()
        dlg = preferences.PreferencesDialogClass(None, -1, "",self.dlgPos, db=self.db)
        v = dlg.ShowModal()
        if v == wx.ID_OK:
            x = dlg.OPanel.changes
            print x
            if 'TabKey' in x:
                val = x['TabKey']
                if val == 0:
                    SetTabIndents = 1
                    SetUseTabs = 1
                elif val == 1:
                    SetTabIndents = 1
                    SetUseTabs = 0
                elif val == 2:
                    SetTabIndents = 0
                    SetUseTabs = 0
                for i in self.docs:
                    i.SetTabIndents(SetTabIndents)
                    i.SetUseTabs(SetUseTabs)
                self.db.ChangeSetting('SetTabIndents',str(SetTabIndents))
                self.db.ChangeSetting('SetUseTabs',str(SetUseTabs))
            if 'SetTabWidth' in x:
                val = x['SetTabWidth']
                for i in self.docs:
                    i.SetTabWidth(int(val))
                self.db.ChangeSetting('SetTabWidth', str(val))
            if 'SetIndent' in x:
                val = x['SetIndent']
                for i in self.docs:
                    i.SetIndent(int(val))
                self.db.ChangeSetting('SetIndent', str(val))
            if 'SetBackSpaceUnIndents' in x:
                val = x['SetBackSpaceUnIndents']
                for i in self.docs:
                    i.SetBackSpaceUnIndents(val)
                self.db.ChangeSetting('SetBackSpaceUnIndents',str(val))
            if 'HomeKeyOps' in x:
                val = x['HomeKeyOps']
                for i in self.docs:
                    if val == 0:
                        i.CmdKeyAssign(wx.stc.STC_KEY_HOME, 0, wx.stc.STC_CMD_DOCUMENTSTART)
                        i.CmdKeyAssign(wx.stc.STC_KEY_END, 0, wx.stc.STC_CMD_DOCUMENTEND)
                    else:
                        i.CmdKeyAssign(wx.stc.STC_KEY_HOME, 0, wx.stc.STC_CMD_HOME)
                        i.CmdKeyAssign(wx.stc.STC_KEY_END, 0, wx.stc.STC_CMD_LINEEND)
                self.db.ChangeSetting('HomeKeyOps', str(val))
            if 'SetScrollWidth' in x:
                val = x['SetScrollWidth']
                for i in self.docs:
                    i.SetScrollWidth = val
                self.db.ChangeSetting('SetScrollWidth',str(val))
        self.dlgPos = dlg.GetScreenPosition()
        dlg.Destroy()
        self.docs[p].SetFocus()

    def getPreference(self, setting, tp):
        ln = 'SELECT value FROM settings WHERE setting = "'+setting+'";'
        v = self.db.cur.execute(ln)
        v1 = v.fetchone()[0]
        if tp == 'Boolean':
            if (v1 == u'0'):
                rt = False
            else:
                rt = True
        elif tp == 'Int':
            rt = int(v1)
        else:
            rt = str(v1)
        return rt

    def SelectOldDocument(self, evt):
        pos = evt.GetId()-1081
        self.LoadFile(self.oldDocs[pos])

    def LoadSession(self, evt):
        mId = evt.GetId()
        sess = self.m1b.GetLabel(mId)
        d = self.db.GetSessionFiles(sess)
        c = self.GetPaths()
        for i in d:
            if str(i) not in c:
                self.Menu101(None)
                p = self.nb.GetSelection()
                doc = self.docs[p]
                # load file in self.path
                doc.LoadFile(i)
                doc.fline, doc.name = os.path.split(i)
                self.nb.SetPageText(p, doc.name)
                # now add to db
                self.db.AddFile(i)
                doc.empty = False

    def ClearOldDocsMenu(self, evt):
        # change db
        self.db.ClearAllOldDocs()
        # change menu structure
        for i in range(1081, 1081 + len(self.oldDocs)):
            self.m1a.Remove(i)
        # remove all old docs
        self.oldDocs = []

    def ChangeLanguage(self, evt):
        id = evt.GetId() - 1601
        l = languages[id]
        p = self.nb.GetSelection()
        doc = self.docs[p]
        doc.langchoice = l
        if l == 'Ada':
            doc.language = lang.SetAsAda(doc)
        elif l == 'Python':
            doc.language = lang.SetAsPython(doc)
        elif l == 'HTML':
            doc.language = lang.SetAsHTML(doc)
        elif l == 'C++':
            doc.language = lang.SetAsCPP(doc)
        elif l == 'LaTeX':
            doc.language = lang.SetAsLatex(doc)
        elif l == 'Lisp':
            doc.language = lang.SetAsLisp(doc)
        elif l == 'Assembler':
            doc.language = lang.SetAsASM(doc)
        elif l == 'Fortran':
            doc.language = lang.SetAsFortran(doc)
        elif l == 'CSS':
            doc.language = lang.SetAsCSS(doc)
        elif l == 'Visual Basic':
            doc.language = lang.SetAsVisualBasic(doc)
        elif l == 'MatLab':
            doc.language = lang.SetAsMatlab(doc)
        elif l == 'Makefile':
            doc.language = lang.SetAsMake(doc)
        elif l == 'Eiffel':
            doc.language = lang.SetAsEiffel(doc)
        elif l == 'Diff':
            doc.language = lang.SetAsDiff(doc)
        elif l[0:4] == 'Conf':
            doc.language = lang.SetAsConf(doc)
        elif l == 'Batch':
            doc.language = lang.SetAsBatch(doc)
        elif l == 'TCL/Tk':
            doc.language = lang.SetAsTCL(doc)
        elif l == 'Ruby':
            doc.language = lang.SetAsRuby(doc)
        elif l == 'SQL':
            doc.language = lang.SetAsSQL(doc)


    def CloseThis(self, evt):
        x, y = self.GetClientSize()
        self.db.ChangeSetting('width', str(x))
        self.db.ChangeSetting('height', str(y))
        # record in db
        x, y = self.GetScreenPosition()
        self.db.ChangeSetting('xpos', str(x))
        self.db.ChangeSetting('ypos', str(y))
        self.db.ChangeSetting('dlgXPos', str(self.dlgPos[0]))
        self.db.ChangeSetting('dlgYPos', str(self.dlgPos[1]))
        # record position & size and store in db
        # store last path used and store in db
        #sys.exit() # delete this when ready
        """
        for p in range(len(self.docs), 0, -1):
            try:
                i = self.docs[p]
                if i.GetModify():
                    # prompt for save
                    self.nb.SetSelection(p)
                    dlg = wx.MessageDialog(self, "This file is not saved! Do you want to save it now?",
                                           "Unsaved file", style=wx.YES_NO | wx.CANCEL | wx.ICON_EXCLAMATION)
                    rtnval = dlg.ShowModal()
                    if (rtnval == wx.ID_YES):
                        # check if it has a name first
                        if self.names[p] == "":
                            # has no name
                            self.docs[p].SaveAsFileMethod()
                        else:
                            self.docs[p].SaveFileMethod()
                    elif (rtnval == wx.ID_NO):
                        self.names.pop(p)
                        self.docs.pop(p)
                        self.nb.RemovePage(p)
                else:
                    self.Menu104(None)
            except IndexError:
                continue
        """
        evt.Skip()

    def GetPaths(self):
        d = []
        for i in self.docs:
            d.append(os.path.join(i.fline, i.name))
        return d

class Application(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)

    def OnInit(self):
        self.db = settings.database()
        self.win = EdWin(None, -1, self.db)
        self.win.Show()
        for f in sys.argv[1:]:
            self.OpenFileMessage(f)
        self.win.docs[0].SetFocus()
        return True

    def BringWindowToFront(self):
        try:
            self.GetTopWindow().Raise()
        except:
            pass

    def OnActivate(self, evt):
        if evt.GetActive():
            self.BringWindowToFront()
        evt.Skip()

    def OpenFileMessage(self, filename):
        fline, fname = os.path.split(filename)
        self.win.LoadFile(filename)

    def MacOpenFile(self, fname):
        self.OpenFileMessage(fname)

    def MacReopenApp(self):
        self.BringWindowToFront()

    def OnExit(self):
        self.db.ChangeSetting('cleanShutdown','True')
        print "ending cleanly na"
        #sys.exit()


if __name__ == '__main__':
    prog = Application(0)
    prog.MainLoop()
