import wx

class Preferences(wx.Dialog):
    def __init__(self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition):
        wx.Dialog.__init__(self, parent, ID, title)
        p1 = wx.Panel(self)
        self.nbt = wx.Notebook(p1)
        self.nbt.AddPage(wx.Panel(self.nbt), "Interface")
        cancelButton = wx.Button(self, 881, "Cancel")
        mainBox = wx.BoxSizer(wx.HORIZONTAL)
        mainBox.Add(self.nbt, 1, wx.EXPAND)
        mainBox.Add(cancelButton, 0)


if __name__ == "__main__":
    prog = wx.PySimpleApp(0)
    x = Preferences(None, 01, "Preferences")
    x.Show()
    prog.MainLoop()
