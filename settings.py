# settings.py
# (c) 2009, Alan James Salmoni, Thought Into Design
# for the Tided text editor for OS X

import os
import os.path
import getpass
import sqlite3
import time
import wx

user = getpass.getuser()
pth = os.path.expanduser('~')
if wx.Platform == '__WXMSW__':
    import ctypes
    import ctypes.wintypes as w1
    w2 = ctypes.windll
    pb = w1.create_unicode_buffer(w1.MAX_PATH)
    res = w2.shell32.SHGetFolderPathW(0,28,0,0,pb)
    APPDIR = pb.value
    print "Windows APPDIR = ",APPDIR
elif wx.Platform == '__WXMAC__':
    APPDIR = '/Users/'+user+'/Library/Application Support/tided/'
else:
    APPDIR = "/home/"+user+"/."


class database(object):
    def __init__(self):
        # test if db already exists... /Users/<name>/Library/Application Support/<tided/config.txt
        self.cs = ['SetUseTabs','SetIndentationGuides','SetIndent','SetViewEOL','SetEOLMode',
              'SetBackSpaceUnIndents',
              'SetCaretForeground','SetOvertype','SetScrollWidth',
              'SetTabIndents','SetTabWidth','SetViewWhiteSpace','SetWrapMode',
              'ViewStatusBar','ViewToolBar','ViewHorizontalScrollBar','ViewVerticalScrollBar',
			  'ViewLineNumbers','ViewFolding','HomeKeyOps','width','height','xpos','ypos',
              'lastPath','dlgXPos','dlgYPos','cleanShutdown'
              ]
        self.vals = ['0','1','4','0','1','1','#000000','0','2000','1','4','0',
                    '0','0,','1','0','1','1','1','0','450','300','20','20', pth,
                    -1, -1, '1']
        self.dbloc = APPDIR
        if not os.path.exists(self.dbloc):
            os.mkdir(self.dbloc)
        self.dbloc = APPDIR+"config.db"
        if os.path.exists(self.dbloc):
            self.exists = True
            self.ConnectToDB()
            self.CheckDBFields()
        else:
            self.exists = False
            self.NewDB()

    def CheckDBFields(self):
        ln = 'SELECT * FROM settings;'
        x = self.cur.execute(ln).fetchall()
        self.fieldList = []
        for i in x:
            self.fieldList.append(i[0])
        for i in range(len(self.cs)):
            if self.cs[i] not in self.fieldList:
                ln = "INSERT INTO settings VALUES ('%s', '%s');"%(self.cs[i], self.vals[i])
                self.cur.execute(ln)
        self.db.commit()

    def GetPreference(self, setting, tp):
        ln = 'SELECT value FROM settings WHERE setting = "'+setting+'";'
        v = self.cur.execute(ln)
        v1 = v.fetchone()[0]
        if tp == 'Boolean':
            if (v1 == u'0') or (v1 == False) or (v1 == 'False'):
                rt = False
            else:
                rt = True
        elif tp == 'Int':
            rt = int(v1)
        else:
            rt = str(v1)
        return rt

    def ConnectToDB(self):
        # connects to an existing database
        try:
            self.db = sqlite3.connect(self.dbloc)
            self.cur = self.db.cursor()
        except:
            self.NewDB()
        # retrieve settings
        

    def NewDB(self):
        # creates the DB from new
        try:
            self.db = sqlite3.connect(self.dbloc)
            self.cur = self.db.cursor()
        except:
            print "Failed to create database"
            # maybe halt program here?
        ln = """CREATE TABLE settings (
                setting     VARCHAR(25),
                value       VARCHAR(20) );
                """
        self.cur.execute(ln)
        ln = """CREATE TABLE docs (
                location     VARCHAR(100),
                wwhen        VARCHAR(20) );
                """
        self.cur.execute(ln)
        ln = """CREATE TABLE files (
                sessionname  VARCHAR(50),
                location     VARCHAR(100) );
                """
        self.cur.execute(ln)
        ln = """CREATE TABLE sessions (
                name         VARCHAR(50),
                timestamp    VARCHAR(20) );
                """
        self.cur.execute(ln)
        self.db.commit()
        for i in range(len(self.cs)):
            ln = "INSERT INTO settings VALUES ('%s', '%s');"%(self.cs[i], self.vals[i])
            self.cur.execute(ln)
        self.db.commit()

    def GetDocs(self):
        ln = 'SELECT location FROM docs;'
        v = self.cur.execute(ln)
        v1 = v.fetchall()
        d = []
        for i in v1:
            d.append(i[0])
        return d

    def GetSessions(self):
        ln = 'SELECT name FROM sessions;'
        v = self.cur.execute(ln)
        v1 = v.fetchall()
        d = []
        for i in v1:
            d.append(i[0])
        return d

    def GetSessionFiles(self, sess):
        ln = 'SELECT location FROM files WHERE sessionname = "'+sess+'";'
        v = self.cur.execute(ln)
        v1 = v.fetchall()
        d = []
        for i in v1:
            d.append(i[0])
        return d

    def SaveSession(self, docs):
        check = True
        for i in docs.docs:
            if i.empty == False:
                check = False
        if check == False:
            sname = time.asctime() # use timestamp as name for now for expedience
            stime = sname
            ln = 'INSERT INTO sessions VALUES ("'+sname+'", "'+stime+'");'
            self.cur.execute(ln)
            for i in docs.docs:
                try:
                    if (i.empty == False):
                        ln = 'INSERT INTO files VALUES ("'+sname+'", "'+i.path+'");'
                        self.cur.execute(ln)
                except AttributeError:
                    ln = ''
            self.db.commit()

    def ClearAllOldDocs(self):
        ln = 'DELETE FROM docs;'
        self.cur.execute(ln)
        self.db.commit()

    def AddFile(self, fID):
        ln = 'SELECT * FROM docs;'
        v = self.cur.execute(ln)
        v1 = v.fetchall()
        repFlag = False
        for i in v1:
            loc = i[0]
            ind = i[1]
            if (loc == fID):
                # delete loc
                ln = 'DELETE FROM docs WHERE location = "'+fID+'";'
                self.cur.execute(ln)
                self.db.commit()
                repFlag = True
                break
        # put doc onto top
        x = time.asctime()
        ln = 'INSERT INTO docs VALUES ("'+fID+'", "'+x+'");'
        self.cur.execute(ln)
        self.db.commit()
        pass

    def ChangeSetting(self, cs, val):
        ln = 'UPDATE settings SET value = "'+val+'" WHERE setting = "'+cs+'";'
        self.cur.execute(ln)
        self.db.commit()

if __name__ == '__main__':
    d = database()
