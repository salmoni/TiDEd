"""
languages.py - a module to set styles for different languages for Tided
(c) 2009, Alan James Salmoni
for
Thought Into Design
"""

import keyword
import wx
import wx.stc as stc


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
                          'mono' : 'Courier',
                          'helv' : 'Lucida Sans',
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

class Styles(object):
    def __init__(self):
        self.s0 = "fore:#808080,face:%(helv)s,size:%(size)d" % faces
        self.s1 = "fore:#007F00,face:%(other)s,size:%(size)d" % faces
        self.s2 = "fore:#007F7F,size:%(size)d" % faces
        self.s3 = "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces
        self.s4 = "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces
        self.s5 = "fore:#00007F,bold,size:%(size)d" % faces
        self.s6 = "fore:#7F0000,size:%(size)d" % faces
        self.s7 = "fore:#7F0000,size:%(size)d" % faces
        self.s8 = "fore:#0000FF,bold,underline,size:%(size)d" % faces
        self.s9 = "fore:#007F7F,bold,size:%(size)d" % faces
        self.s10 = "bold,size:%(size)d" % faces
        self.s11 = "fore:#000000,face:%(helv)s,size:%(size)d" % faces
        self.s12 = "fore:#7F7F7F,size:%(size)d" % faces
        self.s13 = "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces
        self.s14 = "fore:#407090,face:%(helv)s,size:%(size)d" % faces
        self.s15 = "fore:#805000,face:%(helv)s,size:%(size)d" % faces
        self.s16 = "fore:#FFDF00,face:%(helv)s,size:%(size)d" % faces
        self.s17 = "fore:#FFDF00,face:%(helv)s,size:%(size)d" % faces
        self.s18 = "fore:#0000FF,back:#FFEFBF,face:%(helv)s,size:%(size)d" % faces
        self.s19 = "fore:#FF00FF,back:#FFEFFF,face:%(helv)s,size:%(size)d" % faces
        self.s20 = "fore:#000000,back:#FFFFD0,face:%(helv)s,size:%(size)d" % faces
        self.s21 = "fore:#000080,back:#EFEFFF,face:%(helv)s,size:%(size)d" % faces
        self.s22 = "fore:#000080,back:#EFEFFF,bold,face:%(helv)s,size:%(size)d" % faces
        self.s23 = "fore:#006600,back:#EFEFFF,face:%(helv)s,size:%(size)d" % faces
        self.s24 = "fore:#800000,back:#FF6666,face:%(helv)s,size:%(size)d" % faces
        self.s25 = "fore:#993300,back:#EFEFFF,face:%(helv)s,size:%(size)d" % faces
        self.s26 = "fore:#800000,back:#FF6666,face:%(helv)s,size:%(size)d" % faces
        self.s27 = "fore:#3366FF,back:#EFEFFF,face:%(helv)s,size:%(size)d" % faces
        self.s28 = "fore:#333333,back:#EFEFFF,face:%(helv)s,size:%(size)d" % faces
        self.s29 = "fore:#808000,back:#EFEFFF,face:%(helv)s,size:%(size)d" % faces
        self.s30 = ""
        self.s31 = "fore:#000066,back:#CCCCE0,face:%(helv)s,size:%(size)d" % faces
        self.s32 = ""
        self.s33 = ""
        self.s34 = "fore:#0000FF,bold,face:%(helv)s,size:%(size)d" % faces
        self.s35 = "fore:#FF0000,bold,face:%(helv)s,size:%(size)d" % faces
        self.s40 = "fore:#7F7F00,face:%(helv)s,size:%(size)d" % faces
        self.s41 = "fore:#000000,bold,face:%(helv)s,size:%(size)d" % faces
        self.s46 = "fore:#000000,face:%(helv)s,size:%(size)d" % faces
        self.s51 = "fore:#BFBBB0,face:%(helv)s,size:%(size)d" % faces
        self.s52 = "fore:#FFBBB0,face:%(helv)s,size:%(size)d" % faces

        # proxy for testing
        self.s99 = "fore:#ffffff,back:#000000"
        # default - dark grey
        self.s100 = "fore:#000000"
        # word - keywords
        self.s101 = "fore:#002C94"
        # class name, dark blue, underlined
        self.s102 = "fore:#002C94,bold,underline"
        # method / function name, lighter blue, underlined
        self.s103 = "fore:#002C94,bold"
        # identifier (eg, parameters for function)
        self.s104 = "fore:#000000"
        # operators 
        self.s105 = "fore:#222222"
        # all strings
        self.s106 = "fore:#57001A"
        # all comments
        self.s107 = "fore:#00573D"
        # numbers
        self.s108 = "fore:#940076"

s = Styles()

class LanguageObject(object):
    def __init__(self, language, executable, keywords):
        self.language = language
        self.executable = executable
        self.keywords = keywords
def SetAsPython(STC):
    STC.SetKeyWords(0, " ".join(keyword.kwlist))
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_PYTHON)
    
    STC.StyleSetSpec(stc.STC_P_DEFAULT, s.s100)
    STC.StyleSetSpec(stc.STC_P_CLASSNAME, s.s102)
    STC.StyleSetSpec(stc.STC_P_WORD, s.s101)
    STC.StyleSetSpec(stc.STC_P_WORD2, s.s101)
    STC.StyleSetSpec(stc.STC_P_DEFNAME, s.s103)
    STC.StyleSetSpec(stc.STC_P_OPERATOR, s.s105)
    STC.StyleSetSpec(stc.STC_P_IDENTIFIER, s.s104)
    STC.StyleSetSpec(stc.STC_P_CHARACTER, s.s106)
    STC.StyleSetSpec(stc.STC_P_TRIPLE, s.s106)
    STC.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, s.s106)
    STC.StyleSetSpec(stc.STC_P_STRING, s.s106)
    STC.StyleSetSpec(stc.STC_P_STRINGEOL, s.s106)
    STC.StyleSetSpec(stc.STC_P_COMMENTBLOCK, s.s107)
    STC.StyleSetSpec(stc.STC_P_COMMENTLINE, s.s107)
    STC.StyleSetSpec(stc.STC_P_NUMBER, s.s108)
    STC.StyleSetSpec(stc.STC_P_DECORATOR, s.s103)
    """
    STC.StyleSetSpec(stc.STC_P_CHARACTER, s.s4)
    STC.StyleSetSpec(stc.STC_P_CLASSNAME, s.s8)
    STC.StyleSetSpec(stc.STC_P_COMMENTBLOCK, s.s12)
    STC.StyleSetSpec(stc.STC_P_COMMENTLINE, s.s1)
    STC.StyleSetSpec(stc.STC_P_DECORATOR, s.s14)
    STC.StyleSetSpec(stc.STC_P_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_P_DEFNAME, s.s9)
    STC.StyleSetSpec(stc.STC_P_IDENTIFIER, s.s11)
    STC.StyleSetSpec(stc.STC_P_NUMBER, s.s2)
    STC.StyleSetSpec(stc.STC_P_OPERATOR, s.s10)
    STC.StyleSetSpec(stc.STC_P_STRING, s.s3)
    STC.StyleSetSpec(stc.STC_P_STRINGEOL, s.s13)
    STC.StyleSetSpec(stc.STC_P_TRIPLE, s.s6)
    STC.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, s.s7)
    STC.StyleSetSpec(stc.STC_P_WORD, s.s5)
    STC.StyleSetSpec(stc.STC_P_WORD2, s.s15)
    """
    l = LanguageObject("Python", "python", keyword.kwlist)
    return l

def SetAsLatex(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_LATEX)
    STC.StyleSetSpec(stc.STC_L_COMMAND, s.s1)
    STC.StyleSetSpec(stc.STC_L_COMMENT, s.s4)
    STC.StyleSetSpec(stc.STC_L_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_L_MATH, s.s3)
    STC.StyleSetSpec(stc.STC_L_TAG, s.s2)
    return "latex"


def SetAsASM(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_ASM)
    # CHARACTER
    # COMMENT
    # COMMENTBLOCK
    # CPUINSTRUCTION
    # DEFAULT
    # DIRECTIVE
    # DIRECTIVEOPERAND
    # EXTINSTRUCTION
    # IDENTIFIER
    # MATHINSTRUCTION
    # NUMBER
    # OPERATOR
    # REGISTER
    # STRING
    # STRINGEOL
    # return "asm"


def SetAsFortran(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_FORTRAN)
    # CONTINUATION
    # COMMENT
    # DEFAULT
    # IDENTIFIER
    # LABEL
    # NUMBER
    # OPERATOR
    # OPERATOR2
    # PREPROCESSOR
    # STRING1
    # STRING2
    # STRINGEOL
    # WORD
    # WORD2
    # WORD3
    # return "f77"


def SetAsCSS(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_CSS)
    STC.StyleSetSpec(stc.STC_CSS_ATTRIBUTE, s.s16)
    STC.StyleSetSpec(stc.STC_CSS_CLASS, s.s2)
    STC.StyleSetSpec(stc.STC_CSS_COMMENT, s.s9)
    STC.StyleSetSpec(stc.STC_CSS_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_CSS_DIRECTIVE, s.s12)
    STC.StyleSetSpec(stc.STC_CSS_DOUBLESTRING, s.s13)
    STC.StyleSetSpec(stc.STC_CSS_ID, s.s10)
    STC.StyleSetSpec(stc.STC_CSS_IDENTIFIER, s.s6)
    STC.StyleSetSpec(stc.STC_CSS_IDENTIFIER2, s.s15)
    STC.StyleSetSpec(stc.STC_CSS_IMPORTANT, s.s11)
    STC.StyleSetSpec(stc.STC_CSS_OPERATOR, s.s5)
    STC.StyleSetSpec(stc.STC_CSS_PSEUDOCLASS, s.s3)
    STC.StyleSetSpec(stc.STC_CSS_SINGLESTRING, s.s14)
    STC.StyleSetSpec(stc.STC_CSS_TAG, s.s1)
    STC.StyleSetSpec(stc.STC_CSS_UNKNOWN_IDENTIFIER, s.s7)
    STC.StyleSetSpec(stc.STC_CSS_UNKNOWN_PSEUDOCLASS, s.s4)
    STC.StyleSetSpec(stc.STC_CSS_VALUE, s.s8)
    return ""

def SetAsVisualBasic(STC):
    STC.SetKeyWords(0, "AppActivate Base Beep Begin Call Case ChDir ChDrive Const Declare "
            "DefByte DefCur DefDate DefDbl DefDec DefInt DefLng DefObj DefSng "
            "DefStr Deftype DefVar DeleteSetting Dim Do Else End Enum Erase "
            "Event Exit Explicit FileCopy For ForEach Function Get GoSub GoTo "
            "If Implements Kill Let LineInput Lock LSet MkDir Name Next "
            "On Option Private Property Public Put RaiseEvent Randomize ReDim "
            "Rem Reset Resume Return RmDir RSet SavePicture SaveSetting With "
            "SendKeys SetAttr Static Sub Then Type Unlock Wend While Width "
            "Write Height DefBool OnError ")
    STC.SetKeyWords(1, "Abs Array Asc AscB AscW Atn Avg CBool CByte CCur CDate CDbl "
              "Choose Chr ChrB ChrW CInt CLng Command Cos Count CreateObject "
              "CSng CStr CurDir CVar CVDate CVErr Date DateAdd DateDiff Cdec "
              "DatePart DateSerial DateValue Day DDB Dir DoEvents Environ EOF "
              "Error Exp FileAttr FileDateTime FileLen Fix Format FreeFile FV "
              "GetAllStrings GetAttr GetAutoServerSettings GetObject NPV "
              "Hex Hour IIf IMEStatus Input InputB InputBox InStr InstB Int "
              "IPmt IsArray IsDate IsEmpty IsError IsMissing IsNull IsNumeric "
              "IsObject LBound LCase Left LeftB Len LenB LoadPicture Loc LOF "
              "Log LTrim Max Mid MidB Min Minute MIRR Month MsgBox Now NPer "
              "Oct Partition Pmt PPmt PV QBColor Rate RGB Right RightB Rnd "
              "RTrim Second Seek Sgn Shell Sin SLN Space Spc Sqr StDev StDevP "
              "Str StrComp StrConv String Switch Sum SYD Tab Tan Time Timer "
              "TimeSerial TimeValue Trim TypeName UBound UCase Val Var VarP "
              "VarType Weekday Year GetSetting ")
    STC.SetKeyWords(2, "Accept Activate Add AddCustom AddFile AddFromFile AddItem "
              "AddFromTemplate AddNew AddToAddInToolbar AddToolboxProgID "
              "Append AppendChunk Arrange Assert AsyncRead BatchUpdate "
              "BeginTrans Bind Cancel CancelAsyncRead CancelBatch CancelUpdate "
              "CanPropertyChange CaptureImage CellText CellValue Circle Clear "
              "ClearFields ClearSel ClearSelCols Clone Close Cls ColContaining "
              "ColumnSize CommitTrans CompactDatabase Compose Connect Copy "
              "CopyQueryDef CreateDatabase CreateDragImage CreateEmbed "
              "CreateField CreateGroup CreateIndex CreateLink Customize"
              "CreatePreparedStatement CreatePropery CreateQueryCreateQueryDef "
              "CreateRelation CreateTableDef CreateUser CreateWorkspace "
              "Delete DeleteColumnLabels DeleteColumns DeleteRowLabels Open "
              "DeleteRows DoVerb Drag Draw Edit EditCopy EditPaste EndDoc "
              "EnsureVisible EstablishConnection Execute ExtractIcon Fetch "
              "FetchVerbs Files FillCache Find FindFirst FindItem FindLast "
              "FindNext GoForward KillDoc LoadFile MakeCompileFile MoveNext "
              "FindPrevious Forward GetBookmark GetChunk GetClipString GetData "
              "GetFirstVisible GetFormat GetHeader GetLineFromChar GetNumTicks "
              "GetRows GetSelectedPart GetText GetVisibleCount GoBack OLEDrag "
              "Hide HitTest HoldFields Idle InitializeLabels InsertRows Item "
              "InsertColumnLabels InsertColumns InsertObjDlg InsertRowLabels "
              "Layout Line LinkExecute LinkPoke LinkRequest LinkSend Listen "
              "LoadResData LoadResPicture LoadResString LogEvent OpenResultset "
              "MakeReplica MoreResults Move MoveData MoveFirst MoveLast Point "
              "MovePrevious NavigateTo NewPage NewPassword NextRecordset Quit "
              "OnAddinsUpdate OnConnection OnDisconnection OnStartupComplete "
              "OpenConnection OpenDatabase OpenQueryDef OpenRecordset Reload "
              "OpenURL Overlay PaintPicture Paste PastSpecialDlg PeekData Play "
              "PopulatePartial PopupMenu Print PrintForm PropertyChanged PSet "
              "Raise RandomDataFill RandomFillColumns RandomFillRows Remove "
              "rdoCreateEnvironment rdoRegisterDataSource ReadFromFile "
              "Rebind ReFill Refresh RefreshLink RegisterDatabase ReadProperty "
              "RemoveAddInFromToolbar RemoveItem Render RepairDatabase Reply "
              "ReplyAll Requery ResetCustom ResetCustomLabel ResolveName "
              "RestoreToolbar Resync Rollback RollbackTrans RowBookmark "
              "RowContaining RowTop Save SaveAs SaveFile SaveToFile SelectAll "
              "SaveToolbar SaveToOle1File Scale ScaleX ScaleY Scroll Select "
              "SelectPart SelPrint Send SendData Set SetAutoServerSettings "
              "SetData SetFocus SetOption SetSize SetText SetViewport Show "
              "ShowColor ShowFont ShowHelp ShowOpen ShowPrinter ShowSave "
              "ShowWhatsThis SignOff SignOn Size Span SplitContaining "
              "StartLabelEdit StartLogging Stop Synchronize TextHeight "
              "TextWidth ToDefaults TwipsToChartPart TypeByChartType "
              "Update UpdateControls UpdateRecord UpdateRow Upto WhatsThisMode "
              "WriteProperty ZOrder")
    STC.SetKeyWords(3, "AccessKeyPress AfterAddFile AfterChangeFileName AfterCloseFile "
              "AfterColEdit AfterColUpdate AfterDelete AfterInsert "
              "AfterLabelEdit AfterRemoveFile AfterUpdate AfterWriteFile "
              "AmbienChanged ApplyChanges Associate AsyncReadComplete "
              "AxisActivated AxisLabelActivated AxisLabelSelected Collapse "
              "AxisLabelUpdated AxisSelected AxisTitleActivated BeforeColEdit "
              "AxisTitleSelected AxisTitleUpdated AxisUpdated BeforeClick "
              "BeforeColUpdate BeforeConnect BeforeDelete BeforeInsert "
              "BeforeLabelEdit BeforeLoadFile BeforeUpdate ButtonClick "
              "ButtonCompleted ButtonGotFocus ButtonLostFocus Change ColResize "
              "ChartActivated ChartSelected ChartUpdated Click ColEdit "
              "ColumnClick Compare ConfigChageCancelled ConfigChanged "
              "ConnectionRequest DataArrival DataChanged DataUpdated DblClick "
              "Deactivate DeviceArrival DeviceOtherEvent DeviceQueryRemove "
              "DeviceQueryRemoveFailed DeviceRemoveComplete DoGetNewFileName "
              "DeviceRemovePending DevModeChange Disconnect DisplayChanged "
              "Dissociate Done DonePainting DownClick DragDrop DragOver "
              "DropDown EditProperty EnterCell EnterFocus ExitFocus Expand "
              "FootnoteActivated FootnoteSelected FootnoteUpdated GotFocus "
              "HeadClick InfoMessage Initialize IniProperties ItemActivated "
              "ItemAdded ItemCheck ItemClick ItemReloaded ItemRemoved "
              "ItemRenamed ItemSeletected KeyDown KeyPress KeyUp LeaveCell "
              "LegendActivated LegendSelected LegendUpdated LinkClose "
              "LinkError LinkNotify LinkOpen Load LostFocus MouseDown "
              "MouseMove MouseUp NodeClick ObjectMove OLECompleteDrag "
              "OLEDragDrop OLEDragOver OLEGiveFeedback OLESetData OLEStartDrag "
              "OnAddNew OnComm Paint PanelClick PanelDblClick PathChange "
              "PatternChange PlotActivated PlotSelected PlotUpdated "
              "PointActivated Reposition SelChange StateChanged TitleActivated "
              "PointLabelActivated PointLabelSelected PointLabelUpdated "
              "PointSelected PointUpdated PowerQuerySuspend PowerResume "
              "PowerStatusChanged PowerSuspend QueryChangeConfig QueryComplete "
              "QueryCompleted QueryTimeout QueryUnload ReadProperties "
              "RequestChangeFileName RequestWriteFile Resize ResultsChanged "
              "RowColChange RowCurrencyChange RowResize RowStatusChanged "
              "SelectionChanged SendComplete SendProgress SeriesActivated "
              "SeriesSelected SeriesUpdated SettingChanged SplitChange Unload "
              "StatusUpdate SysColorsChanged Terminate TimeChanged "
              "TitleSelected TitleActivated UnboundAddData UnboundDeleteRow "
              "UnboundGetRelativeBookmark UnboundReadData UnboundWriteData "
              "UpClick Updated Validate ValidationError WillAssociate "
              "WillDissociate WillExecute WillUpdateRows WriteProperties "
              "WillChangeData")
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_VB)
    STC.StyleSetSpec(stc.STC_B_ASM, s.s14)
    STC.StyleSetSpec(stc.STC_B_BINNUMBER, s.s18)
    STC.StyleSetSpec(stc.STC_B_COMMENT, s.s1)
    STC.StyleSetSpec(stc.STC_B_CONSTANT, s.s13)
    STC.StyleSetSpec(stc.STC_B_DATE, s.s8)
    STC.StyleSetSpec(stc.STC_B_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_B_ERROR, s.s16)
    STC.StyleSetSpec(stc.STC_B_HEXNUMBER, s.s17)
    STC.StyleSetSpec(stc.STC_B_IDENTIFIER, s.s7)
    STC.StyleSetSpec(stc.STC_B_KEYWORD, s.s3)
    STC.StyleSetSpec(stc.STC_B_KEYWORD2, s.s10)
    STC.StyleSetSpec(stc.STC_B_KEYWORD3, s.s11)
    STC.StyleSetSpec(stc.STC_B_KEYWORD4, s.s12)
    STC.StyleSetSpec(stc.STC_B_LABEL, s.s15)
    STC.StyleSetSpec(stc.STC_B_NUMBER, s.s2)
    STC.StyleSetSpec(stc.STC_B_OPERATOR, s.s6)
    STC.StyleSetSpec(stc.STC_B_PREPROCESSOR, s.s5)
    STC.StyleSetSpec(stc.STC_B_STRING, s.s4)
    STC.StyleSetSpec(stc.STC_B_STRINGEOL, s.s9)
    return "vb"


def SetAsHTML(STC):
    htmlKeywords = (
        "a abbr acronym address applet area b base basefont bdo big blockquote"
        " body br button caption center cite code col colgroup dd del dfn dir"
        " div dl dt em fieldset font form frame frameset h1 h2 h3 h4 h5 h6"
        " head hr html i iframe img input ins isindex kbd label legend li link"
        " map menu meta noframes noscript object ol optgroup option p param"
        " pre q s samp script select small span strike strong style sub sup"
        " table tbody td textarea tfoot th thead title tr tt u ul var xml"
        " xmlns abbr accept-charset accept accesskey action align alink alt"
        " archive axis background bgcolor border cellpadding cellspacing char"
        " charoff charset checked cite class classid clear codebase codetype"
        " color cols colspan compact content coords data datafld dataformatas"
        " datapagesize datasrc datetime declare defer dir disabled enctype"
        " event face for frame frameborder headers height href hreflang hspace"
        " http-equiv id ismap label lang language leftmargin link longdesc"
        " marginwidth marginheight maxlength media method multiple name nohref"
        " noresize noshade nowrap object onblur onchange onclick ondblclick"
        " onfocus onkeydown onkeypress onkeyup onload onmousedown onmousemove"
        " onmouseover onmouseout onmouseup onreset onselect onsubmit onunload"
        " profile prompt readonly rel rev rows rowspan rules scheme scope"
        " selected shape size span src standby start style summary tabindex"
        " target text title topmargin type usemap valign value valuetype"
        " version vlink vspace width text password checkbox radio submit reset"
        " file hidden image public !doctype")
    STC.SetKeyWords(0, htmlKeywords)
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_HTML)
    STC.StyleSetSpec(stc.STC_H_ASP, s.s15)
    STC.StyleSetSpec(stc.STC_H_ASPAT, s.s16)
    STC.StyleSetSpec(stc.STC_H_ATTRIBUTE, s.s3)
    STC.StyleSetSpec(stc.STC_H_ATTRIBUTEUNKNOWN, s.s4)
    STC.StyleSetSpec(stc.STC_H_CDATA, s.s17)
    STC.StyleSetSpec(stc.STC_H_COMMENT, s.s9)
    STC.StyleSetSpec(stc.STC_H_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_H_DOUBLESTRING, s.s6)
    STC.StyleSetSpec(stc.STC_H_ENTITY, s.s10)
    STC.StyleSetSpec(stc.STC_H_NUMBER, s.s5)
    STC.StyleSetSpec(stc.STC_H_OTHER, s.s8)
    STC.StyleSetSpec(stc.STC_H_QUESTION, s.s18)
    STC.StyleSetSpec(stc.STC_H_SCRIPT, s.s14)
    STC.StyleSetSpec(stc.STC_H_SINGLESTRING, s.s7)
    STC.StyleSetSpec(stc.STC_H_TAG, s.s1)
    STC.StyleSetSpec(stc.STC_H_TAGUNKNOWN, s.s2)
    STC.StyleSetSpec(stc.STC_H_VALUE, s.s19)
    return 'open -a Safari'

def SetAsMatlab(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_MATLAB)
    # COMMAND
    STC.StyleSetSpec(stc.STC_MATLAB_COMMAND, "fore:#007F7F,size:%(size)d" % faces)
    # COMMENT
    STC.StyleSetSpec(stc.STC_MATLAB_COMMENT, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
    # DEFAULT
    STC.StyleSetSpec(stc.STC_MATLAB_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
    # IDENTIFIER
    STC.StyleSetSpec(stc.STC_MATLAB_IDENTIFIER, "fore:#7F0000,size:%(size)d" % faces)
    # KEYWORD
    STC.StyleSetSpec(stc.STC_MATLAB_KEYWORD, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    # NUMBER
    STC.StyleSetSpec(stc.STC_MATLAB_NUMBER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    # OPERATOR
    STC.StyleSetSpec(stc.STC_MATLAB_OPERATOR, "fore:#7F0000,size:%(size)d" % faces)
    # STRING
    STC.StyleSetSpec(stc.STC_MATLAB_STRING, "fore:#00007F,bold,size:%(size)d" % faces)
    # DOUBLEQUOTESTRING
    return "matlab"


def SetAsMake(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_LISP)
    # COMMENT
    STC.StyleSetSpec(stc.STC_MAKE_COMMENT, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
    # DEFAULT
    STC.StyleSetSpec(stc.STC_MAKE_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
    # IDENTIFIER
    STC.StyleSetSpec(stc.STC_MAKE_IDENTIFIER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    # IDEOL
    STC.StyleSetSpec(stc.STC_MAKE_IDEOL, "fore:#007F7F,bold,size:%(size)d" % faces)
    # OPERATOR
    STC.StyleSetSpec(stc.STC_MAKE_OPERATOR, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    # PREPROCESSOR
    STC.StyleSetSpec(stc.STC_MAKE_PREPROCESSOR, "fore:#007F7F,size:%(size)d" % faces)
    # TARGET
    STC.StyleSetSpec(stc.STC_MAKE_TARGET, "fore:#00007F,bold,size:%(size)d" % faces)
    return "make"


def SetAsLisp(STC):
    STC.SetKeyWords(0, "abort abs access acons acos acosh add-method adjoin "
                "adjust-array adjustable-array-p alist allocate-instance "
                "alpha-char-p alphanumericp and append apply applyhook apropos "
                "apropos-list aref arithmetic-error arithmetic-error-operands "
                "arithmetic-error-operation array array-dimension "
                "array-dimension-limit array-dimensions array-displacement "
                "array-element-type array-has-fill-pointer-p "
                "array-in-bounds-p array-rank array-rank-limit "
                "array-row-major-index array-total-size "
                "array-total-size-limit arrayp ash asin asinh assert assoc "
                "assoc-if assoc-if-not atan atanh atom backquote baktrace "
                "base-char base-string bignum bignums bit bit-and bit-andc1 "
                "bit-andc2 bit-eqv bit-ior bit-nand bit-nor bit-not bit-orc1 "
                "bit-orc2 bit-vector bit-vector-p bit-xor block boole boole-1 "
                "boole-2 boole-and boole-andc1 boole-andc2 boole-c1 boole-c2 "
                "boole-clr boole-eqv boole-ior boole-nand boole-nor boole-orc1 "
                "boole-orc2 boole-set boole-xor boolean both-case-p boundp "
                "break broadcast-stream broadcast-stream-streams "
                "built-in-class butlast byte byte-position byte-size caaaar "
                "caaadr caaar caadar caaddr caadr caar cadaar cadadr cadar "
                "caddar cadddr caddr cadr call-arguments-limit call-method "
                "call-next-method capitalize car case catch ccase cdaaar "
                "cdaadr cdaar cdadar cdaddr cdadr cdar cddaar cddadr cddar "
                "cdddar cddddr cdddr cddr cdr ceil-error ceil-error-name "
                "ceiling cerror change-class char char-bit char-bits "
                "char-bits-limit char-code char-code-limit char-control-bit "
                "char-downcase char-equal char-font char-font-limit "
                "char-greaterp char-hyper-bit char-int char-lessp "
                "char-meta-bit char-name char-not-equal char-not-greaterp "
                "char-not-lessp char-super-bit char-upcase char/= char<= char= "
                "char>= character characterp check-type cirhash cis class "
                "class-name class-of clear-input clear-output close code-char "
                "coerce commonp compilation-speed compile compile-file "
                "compile-file-pathname compiled-function compiled-function-p "
                "compiler-let compiler-macro compiler-macro-function "
                "complement complex complexp compute-applicable-methods "
                "compute-restarts concatenate concatenated-stream "
                "concatenated-stream-streams cond condition conjugate cons "
                "consp constantly constantp continue control-error copy "
                "copy-list copy-pprint-dispatch copy-readtable copy-seq "
                "copy-structure copy-symbol copy-tree cos cosh count count-if "
                "count-if-not ctypecase debug decf declaim declaration declare "
                "decode-float decode-universal-time defclass defconstant "
                "defgeneric define-compiler-macro define-condition "
                "define-method-combination define-modify-macro "
                "define-setf-expander define-setf-method define-symbol-macro "
                "defmacro defmethod defpackage defparameter defsetf defstruct "
                "deftype defun defvar delete delete-duplicates delete-file "
                "delete-if delete-if-not delete-package denominator "
                "deposite-field describe describe-object destructuring-bind "
                "digit-char digit-char-p directory directory-namestring "
                "disassemble division-by-zero do do* do-all-symbols "
                "do-external-symbols do-symbols dolist dotimes double-float "
                "double-float-epsilon double-float-negative-epsilion dpb "
                "dribble dynamic-extent ecase echo-stream "
                "echo-stream-input-stream echo-stream-output-stream ed eigth "
                "elt encode-universal-time end-of-file endp enough-namestring "
                "ensure-directories-exist ensure-generic-function eq eql equal "
                "equalp error errset etypecase eval eval-when evalhook evenp "
                "every exp export expt extend-char fboundp fceiling "
                "fdefinition fflor fifth file-author file-error "
                "file-error-pathname file-length file-namestring file-position "
                "file-stream file-string-length file-write-date fill "
                "fill-pointer find find-all-symbols find-class find-if "
                "find-if-not find-method find-package find-restart find-symbol "
                "finish-output first fixnum flet float float-digits "
                "float-precision float-radix float-sign floating-point-inexact "
                "floating-point-invalid-operation floating-point-underflow "
                "floatp floor fmakunbound force-output format formatter fourth "
                "fresh-line fround ftruncate ftype funcall function "
                "function-keywords function-lambda-expression functionp gbitp "
                "gcd generic-function gensym gentemp get get-decoded-time "
                "get-dispatched-macro-character get-internal-real-time "
                "get-internal-run-time get-macro-character "
                "get-output-stream-string get-properties get-setf-expansion "
                "get-setf-method get-universial-time getf gethash go "
                "graphic-char-p handler-bind handler-case hash hash-table "
                "hash-table-count hash-table-p hash-table-rehash-size "
                "hash-table-rehash-threshold hash-table-size hash-table-test "
                "host-namestring identity if if-exists ignorable ignore "
                "ignore-errors imagpart import in-package incf "
                "initialize-instance inline input-stream-p inspect int-char "
                "integer integer-decode-float integer-length integerp "
                "interactive-stream-p intern internal-time-units-per-second "
                "intersection invalid-method-error invoke-debugger "
                "invoke-restart invoke-restart-interactively isqrt keyword "
                "keywordp l labels lambda lambda-list-keywords "
                "lambda-parameters-limit last lcm ldb ldb-test ldiff "
                "least-negative-double-float least-negative-long-float "
                "least-negative-normalized-double-float "
                "least-negative-normalized-long-float "
                "least-negative-normalized-short-font "
                "least-negative-normalized-single-font "
                "least-negative-short-font least-negative-single-font "
                "least-positive-double-float least-positive-long-float "
                "least-positive-normalized-double-float "
                "least-positive-normalized-long-float "
                "least-positive-normalized-short-float "
                "least-positive-normalized-single-float "
                "least-positive-short-float least-positive-single-float length "
                "let let* lisp lisp-implementation-type "
                "lisp-implementation-version list list* "
                "list-all-packages list-lenght listen listp load "
                "load-logical-pathname-translation load-time-value locally "
                "log logand logandc1 logandc2 logbitp logcount logeqv "
                "logical-pathname logical-pathname-translations logior lognand "
                "lognor lognot logorc1 logorc2 logtest logxor long-float "
                "long-float-epsilon long-float-negative-epsilon long-site-name "
                "loop loop-finish lower-case-p machine-instance machine-type "
                "machine-version macro-function macroexpand macroexpand-1 "
                "macroexpand-l macrolet make make-array make-broadcast-stream "
                "make-char make-concatenated-stream make-condition "
                "make-dispatch-macro-character make-echo-stream "
                "make-hash-table make-instance make-instances-obsolete "
                "make-list make-load-form make-load-form-saving-slots "
                "make-method make-package make-pathname make-random-state "
                "make-sequence make-string make-string-input-stream "
                "make-string-output-stream make-symbol make-synonym-stream "
                "make-two-way-stream makunbound map map-into mapc mapcan "
                "mapcar mapcon maphash mapl maplist mask-field max member "
                "member-if member-if-not merge merge-pathname merge-pathnames "
                "method method-combination method-combination-error "
                "method-qualifiers min minusp mismatch mod "
                "most-negative-double-float most-negative-fixnum "
                "most-negative-long-float most-negative-short-float "
                "most-negative-single-float most-positive-fixnum "
                "most-positive-long-float most-positive-short-float "
                "most-positive-single-float muffle-warning "
                "multiple-value-bind multiple-value-call multiple-value-limit "
                "multiple-value-list multiple-value-prog1 multiple-value-seteq "
                "multiple-value-setq name name-char namestring nbutlast nconc "
                "next-method-p nil nintersection ninth no-applicable-method "
                "no-next-method not notany notevery notinline nreconc nreverse "
                "nset-difference nset-exclusive-or nstring nstring-capitalize "
                "nstring-downcase nstring-upcase nstubst-if-not nsublis nsubst "
                "nsubst-if nth nth-value nthcdr null number numberp numerator "
                "nunion oddp open open-stream-p optimize or otherwise "
                "output-stream-p package package-error package-error-package "
                "package-name package-nicknames package-shadowing-symbols "
                "package-use-list package-used-by-list packagep pairlis "
                "parse-error parse-integer parse-namestring pathname "
                "pathname-device pathname-directory pathname-host "
                "pathname-match-p pathname-name pathname-type "
                "pathname-version pathnamep peek-char phase pi plist plusp pop "
                "position position-if position-if-not pprint pprint-dispatch "
                "pprint-exit-if-list-exhausted pprint-fill pprint-indent "
                "pprint-linear pprint-logical-block pprint-newline pprint-pop "
                "pprint-tab pprint-tabular prin1 prin1-to-string princ "
                "princ-to-string print print-not-readable "
                "print-not-readable-object print-object probe-file proclaim "
                "prog prog* prog1 prog2 progn program-error progv provide "
                "psetf psetq push pushnew putprop quote random random-state "
                "random-state-p rassoc rassoc-if rassoc-if-not ration rational "
                "rationalize rationalp read read-byte read-car-no-hang "
                "read-char read-delimited-list read-eval-print "
                "read-from-string read-line read-preserving-whitespace "
                "read-squence reader-error readtable readtable-case readtablep "
                "real realp realpart reduce reinitialize-instance rem remf "
                "remhash remove remove-duplicates remove-if "
                "remove-if-not remove-method remprop rename-file "
                "rename-package replace require rest restart restart-bind "
                "restart-case restart-name return return-from revappend "
                "reverse room rotatef round row-major-aref rplaca rplacd "
                "safety satisfies sbit scale-float schar search second "
                "sequence serious-condition set set-char-bit set-difference "
                "set-dispatched-macro-character set-exclusive-or "
                "set-macro-character set-pprint-dispatch "
                "set-syntax-from-char setf setq seventh shadow "
                "shadowing-import shared-initialize shiftf short-float "
                "short-float-epsilon short-float-negative-epsilon "
                "short-site-name signal signed-byte signum simple-array "
                "simple-base-string simple-bit-vector- simple-bit-vector-p "
                "simple-condition simple-condition-format-arguments "
                "simple-condition-format-control simple-error simple-string "
                "simple-string-p simple-type-error simple-vector "
                "simple-vector-p simple-warning sin single-float "
                "single-float-epsilon single-float-negative-epsilon sinh "
                "sixth sleep slot-boundp slot-exists-p slot-makunbound "
                "slot-missing slot-unbound slot-value software-type "
                "software-version some sort space special special-form-p "
                "special-operator-p speed sqrt stable-sort standard "
                "standard-char standard-char-p standard-class "
                "standard-generic-function standard-method standard-object "
                "step storage-condition store-value stream stream-element-type "
                "stream-error stream-error-stream stream-external-format "
                "streamp streamup string string-capitalize string-char "
                "string-char-p string-downcase string-equal string-greaterp "
                "string-left-trim string-lessp string-not-equal "
                "string-not-greaterp string-not-lessp string-right-strim "
                "string-right-trim string-stream string-trim string-upcase "
                "string/= string< string<= string= string> string>= stringp "
                "structure structure-class structure-object style-warning "
                "sublim sublis subseq subsetp subst subst-if subst-if-not "
                "substitute substitute-if substitute-if-not subtypep svref "
                "sxhash symbol symbol-function symbol-macrolet symbol-name "
                "symbol-package symbol-plist symbol-value symbolp "
                "synonym-stream synonym-stream-symbol sys system t tagbody "
                "tailp tan tanh tenth terpri the third throw time trace "
                "translate-logical-pathname translate-pathname tree-equal "
                "truename truncase truncate two-way-stream "
                "two-way-stream-input-stream two-way-stream-output-stream "
                "type type-error type-error-datnum type-error-expected-type "
                "type-of typecase typep unbound-slot unbound-slot-instance "
                "unbound-variable undefined-function unexport unintern union "
                "unless unread unread-char unsigned-byte untrace unuse-package "
                "unwind-protect update-instance-for-different-class "
                "update-instance-for-redefined-class "
                "upgraded-array-element-type upgraded-complex-part-type "
                "upper-case-p use-package use-value user user-homedir-pathname "
                "value value-list values vector vector-pop vector-push "
                "vector-push-extend vectorp warn warning when "
                "wild-pathname-p with-accessors with-compilation-unit "
                "with-condition-restarts with-hash-table-iterator "
                "with-input-from-string with-open-file with-open-stream "
                "with-output-to-string with-package-iterator "
                "with-simple-restart with-slots with-standard-io-syntax write "
                "write-byte write-char write-line write-sequence" )
    STC.SetKeyWords(1, ":abort :adjustable :append :array :base :case :circle "
                    ":conc-name :constructor :copier :count :create :default "
                    ":device :directory :displaced-index-offset :displaced-to "
                    ":element-type :end :end1 :end2 :error :escape :external "
                    ":from-end :gensym :host :include :if-does-not-exist "
                    ":if-exists :index :inherited :internal :initial-contents "
                    ":initial-element :initial-offset :initial-value :input "
                    ":io :junk-allowed :key :length :level :name :named "
                    ":new-version :nicknames :output :ouput=file :overwrite "
                    ":predicate :preserve-whitespace :pretty :print "
                    ":print-function :probe :radix :read-only :rehash-size "
                    ":rehash-threshold :rename :size :rename-and-delete :start "
                    ":start1 :start2 :stream :supersede :test :test-not :use "
                    ":verbose :version")
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_LISP)
    STC.StyleSetSpec(stc.STC_LISP_COMMENT, s.s1)
    STC.StyleSetSpec(stc.STC_LISP_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_LISP_IDENTIFIER, s.s9)
    STC.StyleSetSpec(stc.STC_LISP_KEYWORD, s.s3)
    STC.StyleSetSpec(stc.STC_LISP_KEYWORD_KW, s.s4)
    STC.StyleSetSpec(stc.STC_LISP_MULTI_COMMENT, s.s12)
    STC.StyleSetSpec(stc.STC_LISP_NUMBER, s.s2)
    STC.StyleSetSpec(stc.STC_LISP_OPERATOR, s.s10)
    STC.StyleSetSpec(stc.STC_LISP_SPECIAL, s.s11)
    STC.StyleSetSpec(stc.STC_LISP_STRING, s.s6)
    STC.StyleSetSpec(stc.STC_LISP_STRINGEOL, s.s8)
    STC.StyleSetSpec(stc.STC_LISP_SYMBOL, s.s5)
    return "cl"


def SetAsEiffel(STC):
    STC.SetKeyWords(0, "alias all and any as bit boolean check class character clone " 
        "cluster create creation current debug deferred div do double " 
        "else elseif end ensure equal expanded export external false " 
        "feature forget from frozen general if implies indexing infix " 
        "inherit inspect integer invariant is language like local loop " 
        "mod name nochange none not obsolete old once or platform " 
        "pointer prefix precursor program real redefine rename require " 
        "rescue result retry root select separate string strip then " 
        "true undefine unique until variant void when xor")
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_EIFFEL)
    STC.StyleSetSpec(stc.STC_EIFFEL_CHARACTER, s.s5)
    STC.StyleSetSpec(stc.STC_EIFFEL_COMMENTLINE, s.s1)
    STC.StyleSetSpec(stc.STC_EIFFEL_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_EIFFEL_IDENTIFIER, s.s7)
    STC.StyleSetSpec(stc.STC_EIFFEL_NUMBER, s.s2)
    STC.StyleSetSpec(stc.STC_EIFFEL_OPERATOR, s.s6)
    STC.StyleSetSpec(stc.STC_EIFFEL_STRING, s.s4)
    STC.StyleSetSpec(stc.STC_EIFFEL_STRINGEOL, s.s8)
    STC.StyleSetSpec(stc.STC_EIFFEL_WORD, s.s3)
    return "eiffel"

def SetAsDiff(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_DIFF)
    # ADDED
    STC.StyleSetSpec(stc.STC_DIFF_ADDED, "fore:#7F0000,size:%(size)d" % faces)
    # COMMAND
    STC.StyleSetSpec(stc.STC_DIFF_COMMAND, "fore:#007F7F,size:%(size)d" % faces)
    # COMMENT
    STC.StyleSetSpec(stc.STC_DIFF_COMMENT, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
    # DEFAULT
    STC.StyleSetSpec(stc.STC_DIFF_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
    # DELETED
    STC.StyleSetSpec(stc.STC_DIFF_DELETED, "fore:#00007F,bold,size:%(size)d" % faces)
    # HEADER
    STC.StyleSetSpec(stc.STC_DIFF_HEADER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    # POSITION
    STC.StyleSetSpec(stc.STC_DIFF_POSITION, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    return ""


def SetAsConf(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_CONF)
    # COMMENT
    STC.StyleSetSpec(stc.STC_CONF_COMMENT, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
    # DEFAULT
    STC.StyleSetSpec(stc.STC_CONF_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
    # DIRECTIVE
    STC.StyleSetSpec(stc.STC_CONF_DIRECTIVE, "fore:#007F7F,bold,size:%(size)d" % faces)
    # EXTENSION
    STC.StyleSetSpec(stc.STC_CONF_EXTENSION, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    # IDENTIFIER
    STC.StyleSetSpec(stc.STC_CONF_IDENTIFIER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    # IP
    STC.StyleSetSpec(stc.STC_CONF_IP, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
    # NUMBER
    STC.StyleSetSpec(stc.STC_CONF_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
    # OPERATOR
    STC.StyleSetSpec(stc.STC_CONF_OPERATOR, "fore:#7F0000,size:%(size)d" % faces)
    # PARAMETER
    STC.StyleSetSpec(stc.STC_CONF_PARAMETER, "fore:#00007F,bold,size:%(size)d" % faces)
    # STRING
    STC.StyleSetSpec(stc.STC_CONF_STRING, "fore:#7F0000,size:%(size)d" % faces)
    return ""

def SetAsAda(STC):
    STC.SetKeyWords(0, "abort abstract accept access aliased all array at begin " 
        "body case constant declare delay delta digits do else " 
        "elsif end entry exception exit for function generic goto " 
        "if in is limited loop new null of others out package " 
        "pragma private procedure protected raise range record " 
        "renames requeue return reverse select separate subtype " 
        "tagged task terminate then type until use when while with") 
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_ADA)
    STC.StyleSetSpec(stc.STC_ADA_CHARACTER, s.s5)
    STC.StyleSetSpec(stc.STC_ADA_CHARACTEREOL, s.s6)
    STC.StyleSetSpec(stc.STC_ADA_COMMENTLINE, s.s10)
    STC.StyleSetSpec(stc.STC_ADA_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_ADA_IDENTIFIER, s.s2)
    STC.StyleSetSpec(stc.STC_ADA_ILLEGAL, s.s11)
    STC.StyleSetSpec(stc.STC_ADA_LABEL, s.s9)
    STC.StyleSetSpec(stc.STC_ADA_NUMBER, s.s3)
    STC.StyleSetSpec(stc.STC_ADA_STRING, s.s7)
    STC.StyleSetSpec(stc.STC_ADA_STRINGEOL, s.s8)
    STC.StyleSetSpec(stc.STC_ADA_WORD, s.s11)
    return "gnatmake"


def SetAsASP(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_ASP)


def SetAsBatch(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_BATCH)
    STC.StyleSetSpec(stc.STC_BAT_COMMAND, s.s5)
    STC.StyleSetSpec(stc.STC_BAT_COMMENT, s.s1)
    STC.StyleSetSpec(stc.STC_BAT_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_BAT_HIDE, s.s4)
    STC.StyleSetSpec(stc.STC_BAT_IDENTIFIER, s.s6)
    STC.StyleSetSpec(stc.STC_BAT_LABEL, s.s3)
    STC.StyleSetSpec(stc.STC_BAT_OPERATOR, s.s7)
    STC.StyleSetSpec(stc.STC_BAT_WORD, s.s2)
    return ""

def SetAsTCL(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_TCL)
    STC.StyleSetSpec(stc.STC_TCL_BLOCK_COMMENT, s.s21)
    STC.StyleSetSpec(stc.STC_TCL_COMMENT, s.s1)
    STC.StyleSetSpec(stc.STC_TCL_COMMENTLINE, s.s2)
    STC.StyleSetSpec(stc.STC_TCL_COMMENT_BOX, s.s20)
    STC.StyleSetSpec(stc.STC_TCL_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_TCL_EXPAND, s.s11)
    STC.StyleSetSpec(stc.STC_TCL_IDENTIFIER, s.s7)
    STC.StyleSetSpec(stc.STC_TCL_IN_QUOTE, s.s5)
    STC.StyleSetSpec(stc.STC_TCL_MODIFIER, s.s10)
    STC.StyleSetSpec(stc.STC_TCL_NUMBER, s.s3)
    STC.StyleSetSpec(stc.STC_TCL_OPERATOR, s.s6)
    STC.StyleSetSpec(stc.STC_TCL_SUBSTITUTION, s.s8)
    STC.StyleSetSpec(stc.STC_TCL_SUB_BRACE, s.s9)
    STC.StyleSetSpec(stc.STC_TCL_WORD, s.s2)
    STC.StyleSetSpec(stc.STC_TCL_WORD2, s.s13)
    STC.StyleSetSpec(stc.STC_TCL_WORD3, s.s14)
    STC.StyleSetSpec(stc.STC_TCL_WORD4, s.s15)
    STC.StyleSetSpec(stc.STC_TCL_WORD5, s.s16)
    STC.StyleSetSpec(stc.STC_TCL_WORD6, s.s17)
    STC.StyleSetSpec(stc.STC_TCL_WORD7, s.s18)
    STC.StyleSetSpec(stc.STC_TCL_WORD8, s.s19)
    STC.StyleSetSpec(stc.STC_TCL_WORD_IN_QUOTE, s.s4)
    return "tcl"

def SetAsRuby(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_RUBY)
    STC.StyleSetSpec(stc.STC_RB_BACKTICKS, s.s18)
    STC.StyleSetSpec(stc.STC_RB_CHARACTER, s.s7)
    STC.StyleSetSpec(stc.STC_RB_CLASSNAME, s.s8)
    STC.StyleSetSpec(stc.STC_RB_CLASS_VAR, s.s17)
    STC.StyleSetSpec(stc.STC_RB_COMMENTLINE, s.s2)
    STC.StyleSetSpec(stc.STC_RB_DATASECTION, s.s19)
    STC.StyleSetSpec(stc.STC_RB_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_RB_DEFNAME, s.s9)
    STC.StyleSetSpec(stc.STC_RB_ERROR, s.s1)
    STC.StyleSetSpec(stc.STC_RB_GLOBAL, s.s13)
    STC.StyleSetSpec(stc.STC_RB_HERE_DELIM, s.s20)
    STC.StyleSetSpec(stc.STC_RB_HERE_Q, s.s21)
    STC.StyleSetSpec(stc.STC_RB_HERE_QQ, s.s22)
    STC.StyleSetSpec(stc.STC_RB_HERE_QX, s.s23)
    STC.StyleSetSpec(stc.STC_RB_IDENTIFIER, s.s11)
    STC.StyleSetSpec(stc.STC_RB_INSTANCE_VAR, s.s16)
    STC.StyleSetSpec(stc.STC_RB_MODULE_NAME, s.s15)
    STC.StyleSetSpec(stc.STC_RB_NUMBER, s.s4)
    STC.StyleSetSpec(stc.STC_RB_OPERATOR, s.s10)
    STC.StyleSetSpec(stc.STC_RB_POD, s.s3)
    STC.StyleSetSpec(stc.STC_RB_REGEX, s.s12)
    STC.StyleSetSpec(stc.STC_RB_STDERR, s.s40)
    STC.StyleSetSpec(stc.STC_RB_STDIN, s.s30)
    STC.StyleSetSpec(stc.STC_RB_STDOUT, s.s31)
    STC.StyleSetSpec(stc.STC_RB_STRING, s.s6)
    STC.StyleSetSpec(stc.STC_RB_STRING_Q, s.s24)
    STC.StyleSetSpec(stc.STC_RB_STRING_QQ, s.s25)
    STC.StyleSetSpec(stc.STC_RB_STRING_QR, s.s27)
    STC.StyleSetSpec(stc.STC_RB_STRING_QW, s.s28)
    STC.StyleSetSpec(stc.STC_RB_STRING_QX, s.s26)
    STC.StyleSetSpec(stc.STC_RB_SYMBOL, s.s14)
    STC.StyleSetSpec(stc.STC_RB_UPPER_BOUND, s.s41)
    STC.StyleSetSpec(stc.STC_RB_WORD, s.s5)
    STC.StyleSetSpec(stc.STC_RB_WORD_DEMOTED, s.s29)
    return "ruby"


def SetAsSQL(STC):
    STC.SetKeyWords(0, "access add all alter and any as asc audit between by check "
             "cluster column comment compress connect create current default "
             "delete desc distinct drop else exclusive exists file for from "
             "grant group having identified immediate in increment index "
             "initial insert intersect into is like lock maxextents minus mode "
             "modify noaudit nocompress not nowait number of offline on online "
             "option or order pctfree prior privileges public rename resource "
             "revoke row rows select session set share size start successful "
             "synonym table to trigger union unique update validate values "
             "view whenever where with primary key constraint foreign "
             "references restrict no action without schema deferrable not "
             "deferrable rule do")
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_SQL)
    STC.StyleSetSpec(stc.STC_SQL_CHARACTER, s.s7)
    STC.StyleSetSpec(stc.STC_SQL_COMMENT, s.s1)
    STC.StyleSetSpec(stc.STC_SQL_COMMENTDOC, s.s3)
    STC.StyleSetSpec(stc.STC_SQL_COMMENTDOCKEYWORD, s.s17)
    STC.StyleSetSpec(stc.STC_SQL_COMMENTDOCKEYWORDERROR, s.s18)
    STC.StyleSetSpec(stc.STC_SQL_COMMENTLINE, s.s2)
    STC.StyleSetSpec(stc.STC_SQL_COMMENTLINEDOC, s.s15)
    STC.StyleSetSpec(stc.STC_SQL_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_SQL_IDENTIFIER, s.s11)
    STC.StyleSetSpec(stc.STC_SQL_NUMBER, s.s4)
    STC.StyleSetSpec(stc.STC_SQL_OPERATOR, s.s10)
    STC.StyleSetSpec(stc.STC_SQL_QUOTEDIDENTIFIER, s.s23)
    STC.StyleSetSpec(stc.STC_SQL_SQLPLUS, s.s8)
    STC.StyleSetSpec(stc.STC_SQL_SQLPLUS_COMMENT, s.s13)
    STC.StyleSetSpec(stc.STC_SQL_SQLPLUS_PROMPT, s.s9)
    STC.StyleSetSpec(stc.STC_SQL_STRING, s.s6)
    STC.StyleSetSpec(stc.STC_SQL_USER1, s.s19)
    STC.StyleSetSpec(stc.STC_SQL_USER2, s.s20)
    STC.StyleSetSpec(stc.STC_SQL_USER3, s.s21)
    STC.StyleSetSpec(stc.STC_SQL_USER4, s.s22)
    STC.StyleSetSpec(stc.STC_SQL_WORD, s.s5)
    STC.StyleSetSpec(stc.STC_SQL_WORD2, s.s16)
    return ""


def SetAsRebol(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_REBOL)
    STC.StyleSetSpec(stc.STC_REBOL_BINARY, s.s11)
    STC.StyleSetSpec(stc.STC_REBOL_BRACEDSTRING, s.s7)
    STC.StyleSetSpec(stc.STC_REBOL_CHARACTER, s.s5)
    STC.StyleSetSpec(stc.STC_REBOL_COMMENTBLOCK, s.s2)
    STC.StyleSetSpec(stc.STC_REBOL_COMMENTLINE, s.s1)
    STC.StyleSetSpec(stc.STC_REBOL_DATE, s.s18)
    STC.StyleSetSpec(stc.STC_REBOL_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_REBOL_EMAIL, s.s16)
    STC.StyleSetSpec(stc.STC_REBOL_FILE, s.s15)
    STC.StyleSetSpec(stc.STC_REBOL_IDENTIFIER, s.s20)
    STC.StyleSetSpec(stc.STC_REBOL_ISSUE, s.s13)
    STC.StyleSetSpec(stc.STC_REBOL_MONEY, s.s12)
    STC.StyleSetSpec(stc.STC_REBOL_NUMBER, s.s8)
    STC.StyleSetSpec(stc.STC_REBOL_OPERATOR, s.s4)
    STC.StyleSetSpec(stc.STC_REBOL_PAIR, s.s9)
    STC.StyleSetSpec(stc.STC_REBOL_PREFACE, s.s3)
    STC.StyleSetSpec(stc.STC_REBOL_QUOTEDSTRING, s.s6)
    STC.StyleSetSpec(stc.STC_REBOL_TAG, s.s14)
    STC.StyleSetSpec(stc.STC_REBOL_TIME, s.s19)
    STC.StyleSetSpec(stc.STC_REBOL_TUPLE, s.s10)
    STC.StyleSetSpec(stc.STC_REBOL_URL, s.s17)
    STC.StyleSetSpec(stc.STC_REBOL_WORD, s.s21)
    STC.StyleSetSpec(stc.STC_REBOL_WORD2, s.s22)
    STC.StyleSetSpec(stc.STC_REBOL_WORD3, s.s23)
    STC.StyleSetSpec(stc.STC_REBOL_WORD4, s.s24)
    STC.StyleSetSpec(stc.STC_REBOL_WORD5, s.s25)
    STC.StyleSetSpec(stc.STC_REBOL_WORD6, s.s26)
    STC.StyleSetSpec(stc.STC_REBOL_WORD7, s.s27)
    STC.StyleSetSpec(stc.STC_REBOL_WORD8, s.s28)
    return "rebol"

def SetAsCPP(STC):
    STC.StyleClearAll()
    STC.SetLexer(stc.STC_LEX_CPP)
    STC.StyleSetSpec(stc.STC_C_CHARACTER, s.s7)
    STC.StyleSetSpec(stc.STC_C_COMMENT, s.s1)
    STC.StyleSetSpec(stc.STC_C_COMMENTDOC, s.s3)
    STC.StyleSetSpec(stc.STC_C_COMMENTDOCKEYWORD, s.s17)
    STC.StyleSetSpec(stc.STC_C_COMMENTDOCKEYWORDERROR, s.s18)
    STC.StyleSetSpec(stc.STC_C_COMMENTLINE, s.s2)
    STC.StyleSetSpec(stc.STC_C_COMMENTLINEDOC, s.s15)
    STC.StyleSetSpec(stc.STC_C_DEFAULT, s.s0)
    STC.StyleSetSpec(stc.STC_C_IDENTIFIER, s.s11)
    STC.StyleSetSpec(stc.STC_C_NUMBER, s.s4)
    STC.StyleSetSpec(stc.STC_C_OPERATOR, s.s10)
    STC.StyleSetSpec(stc.STC_C_PREPROCESSOR, s.s9)
    STC.StyleSetSpec(stc.STC_C_REGEX, s.s14)
    STC.StyleSetSpec(stc.STC_C_STRING, s.s6)
    STC.StyleSetSpec(stc.STC_C_STRINGEOL, s.s12)
    STC.StyleSetSpec(stc.STC_C_UUID, s.s8)
    STC.StyleSetSpec(stc.STC_C_VERBATIM, s.s13)
    STC.StyleSetSpec(stc.STC_C_WORD, s.s5)
    STC.StyleSetSpec(stc.STC_C_WORD2, s.s16)

    return "gcc"

