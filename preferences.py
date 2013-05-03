#!/usr/bin/env python2.3
#
#  preferences.py
#  tided project
#
#  Created by Alan James Salmoni on 24/08/09.
#  Copyright (c) 2009 Thought Into Design. All rights reserved.
#

import sys
import wx
import wx.lib.masked as masked
import wx.lib.agw.buttonpanel as bp
import icons

panels = ['Interface', 'Editing', 'Language']


class OptionsPanelClass(wx.Panel):
    def __init__(self, parent, db):
        wx.Panel.__init__(self, parent, -1)
        self.db = db
        self.changes = {}
        self.SetSize((396,379))
        self.tabChoice = ['inserts tabs + spaces', 'inserts spaces only', 'indents']
        self.backspaceChoice = ['deletes character only', 'deletes indent']
        self.homeChoice = ['start/end of document','start/end of line']
        normen = wx.Font(13, wx.SWISS, wx.NORMAL, wx.DEFAULT)
        bolden = wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD)
        l1 = wx.StaticText(self, -1, "Tab Key :", (81,23))#86))
        l2 = wx.StaticText(self, -1, "Backspace :", (65,122))#85))
        l3 = wx.StaticText(self, -1, "Home/end key :", (36,154))
        l4 = wx.StaticText(self, -1, "Document :", (67,187))
        l5 = wx.StaticText(self, -1, "characters per tab", (209,57))
        l6 = wx.StaticText(self, -1, "characters per indent", (209,90))
        l7 = wx.StaticText(self, -1, "pixels width", (215,189))
        l1.SetFont(bolden)
        l2.SetFont(bolden)
        l3.SetFont(bolden)
        l4.SetFont(bolden)
        l5.SetFont(normen)
        l6.SetFont(normen)
        l7.SetFont(normen)
        self.choice1 = wx.Choice(self, 780, pos=(152,21), 
                            size=(198, 21), choices=self.tabChoice)
        self.t1 = masked.TextCtrl(self, -1, "", pos=(173,54), 
                            size=(30, 21), mask='#{2}')
        self.t2 = masked.TextCtrl(self, -1, "", pos=(173,87), 
                            size=(30, 21), mask='#{2}')
        self.t3 = masked.TextCtrl(self, -1, "", pos=(153,186),
                            size=(50,21), mask = '#{5}')
        self.choice2 = wx.Choice(self, 781, pos=(152,120),
                                size=(196, 21), choices=self.backspaceChoice)
        self.choice3 = wx.Choice(self, 782, pos=(152,153),
                                size=(196, 21), choices=self.homeChoice)
        self.b1 = wx.Button(self, 782, "Set the base font...", pos=(153,219),
                                size=(140, 21))
        self.b2 = wx.Button(self, wx.ID_CANCEL, pos=(222,283))
        self.b3 = wx.Button(self, wx.ID_OK, pos=(305,283))
        self.b4 = wx.Button(self, 783, "Reset", pos=(21, 283), size=(70,20))
        self.b3.SetDefault()
        self.Bind(wx.EVT_CHOICE, self.Choice1Changed, self.choice1)
        self.Bind(wx.EVT_CHOICE, self.Choice2Changed, self.choice2)
        self.Bind(wx.EVT_CHOICE, self.Choice3Changed, self.choice3)
        self.Bind(wx.EVT_TEXT, self.t1Changed, self.t1)
        self.Bind(wx.EVT_TEXT, self.t2Changed, self.t2)
        self.Bind(wx.EVT_TEXT, self.t3Changed, self.t3)
        self.Bind(wx.EVT_BUTTON, self.Reset, self.b4)
        self.GetVals()

    def Choice1Changed(self, evt):
        val = self.choice1.GetSelection()
        if val == self.TabKey:
            try:
                del self.changes['TabKey']
            except KeyError:
                pass
        else:
            self.changes['TabKey'] = val

    def Choice2Changed(self, evt):
        val = self.choice2.GetSelection()
        if val == self.TabKey:
            try:
                del self.changes['SetBackSpaceUnIndents']
            except KeyError:
                pass
        else:
            self.changes['SetBackSpaceUnIndents'] = val

    def Choice3Changed(self, evt):
        val = self.choice3.GetSelection()
        if val == self.HomeKeyOps:
            try:
                del self.changes['HomeKeyOps']
            except KeyError:
                pass
        else:
            self.changes['HomeKeyOps'] = val

    def t1Changed(self, evt):
        val = self.t1.GetValue()
        if val == str(self.SetTabWidth):
            del self.changes['SetTabWidth']
        else:
            self.changes['SetTabWidth'] = val

    def t2Changed(self, evt):
        val = self.t2.GetValue()
        if val == str(self.SetIndent):
            del self.changes['SetIndent']
        else:
            self.changes['SetIndent'] = val

    def t3Changed(self, evt):
        val = self.t3.GetValue()
        if val == str(self.SetScrollWidth):
            del self.changes['SetScrollWidth']
        else:
            self.changes['SetScrollWidth'] = val

    def GetVals(self):
        v = self.db.GetPreference('SetTabIndents', 'Boolean')
        w = self.db.GetPreference('SetUseTabs', 'Boolean')
        if v == 0:
            self.TabKey = 2
        elif w == 0:
            self.TabKey = 1
        else:
            self.TabKey = 0
        self.SetTabWidth = self.db.GetPreference('SetTabWidth', 'Int')
        self.SetIndent = self.db.GetPreference('SetIndent', 'Int')
        self.SetBackSpaceUnIndents = self.db.GetPreference('SetBackSpaceUnIndents', 'Boolean')
        self.HomeKeyOps = self.db.GetPreference('HomeKeyOps', 'Boolean')
        self.SetScrollWidth = self.db.GetPreference('SetScrollWidth', 'Int')
        self.Reset(None)

    def Reset(self, evt):
        self.choice1.SetSelection(self.TabKey)
        self.t1.SetValue(str(self.SetTabWidth))
        self.t2.SetValue(str(self.SetIndent))
        self.choice2.SetSelection(self.SetBackSpaceUnIndents)
        self.choice3.SetSelection(self.HomeKeyOps)
        self.t3.SetValue(str(self.SetScrollWidth))
        self.changes = {}
        print "Reset TabWidth to ",self.SetTabWidth


class PreferencesDialogClass(wx.Dialog):
    def __init__(self, parent, id, title, position, db):
        wx.Dialog.__init__(self, parent, id, title, position)
        if position == (-1,-1):
            self.CentreOnParent(wx.BOTH)
        self.db = db
        self.tb = bp.ButtonPanel(self, -1, "")
        self.sizes = [(396,412),(350,450),(400,600)]
        self.OPanel = self.makeOptionsPanel(self)
        opts_img = icons.getoptionsBitmap()
        lang_img = icons.getlanguagesBitmap()
        btn_opts = bp.ButtonInfo(self.tb, 1051, opts_img, text='Options')
        btn_lang = bp.ButtonInfo(self.tb, 1052, lang_img, text='Languages')
        self.tb.AddButton(btn_opts)
        self.tb.AddButton(btn_lang)
        self.vs = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vs)
        self.vs.Add(self.tb, 0, wx.EXPAND)
        self.vs.Add(self.OPanel, 1, wx.EXPAND)
        self.tb.GetBPArt().SetColour(bp.BP_GRADIENT_COLOR_FROM, wx.Colour(255,255,255,255))
        self.tb.GetBPArt().SetColour(bp.BP_GRADIENT_COLOR_TO, wx.Colour(255,255,255,255))
        self.tb.GetBPArt().SetGradientType(bp.BP_GRADIENT_VERTICAL)
        self.tb.SetStyle(bp.BP_USE_GRADIENT)
        self.tb.DoLayout()

        self.SetSize((396,412))
        #self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.ChangeTab)
        #self.Bind(wx.EVT_CLOSE, self.CloseThis, id=909)
        #print "1111 ",type(self.IPanel)

    def ChangeTab(self, evt):
        t = evt.GetSelection()
        self.SetSize(self.sizes[t])

    def makeOptionsPanel(self, parent):
        return OptionsPanelClass(parent, self.db)

if __name__ == '__main__':
	app = wx.PySimpleApp(0)
	win = PreferencesDialogClass(None, -1, "")
	win.ShowModal()
	#app.MainLoop()