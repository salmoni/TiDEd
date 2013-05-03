#!/usr/bin/env python2.3
#
#  toolbar.py
#  tided project
#
#  Created by Alan Salmoni on 5/09/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#


import wx
import wx.aui


class DropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    def OnDropFiles(self, x, y, files):
        print "dropping"
        for i in files:
            self.obj.parent.LoadFile(i)

class NoteBook(wx.aui.AuiNotebook):
    def __init__(self, parent):
        nfdt = DropTarget(self)
        self.SetDropTarget(nfdt)
