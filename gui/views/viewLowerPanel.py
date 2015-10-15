__author__ = 'Francisco'


from gui.views.viewPlot import ViewPlot, ViewPlotForSiteViewer, Data
import wx
from gui.controller.logicDatabase import LogicDatabase
import coordinator.events as engineEvent
from viewContext import TimeSeriesContextMenu, SimulationContextMenu, ConsoleContextMenu
import coordinator.engineAccessors as engine
from wx.lib.pubsub import pub as Publisher
from utilities import db as dbUtilities
from db import dbapi as dbapi
from gui import events
import threading
from wx import richtext
from coordinator.emitLogging import elog
from gui.controller import logicConsoleOutput
import os, sys
from db.ODM1.WebServiceAPI import WebServiceApi
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
import wx.calendar as cal


class viewLowerPanel:
    def __init__(self, notebook):

        # notebook = wx.Notebook

        console = ConsoleTab(notebook)
        timeseries = TimeSeriesTab(notebook)
        simulations = SimulationDataTab(notebook)

        notebook.AddPage(console, "Console")
        notebook.AddPage(timeseries, "Time Series")
        notebook.AddPage(simulations, "Simulations")

        # deactivate the console if we are in debug mode
        if not sys.gettrace():
            # redir = RedirectText(self.log)
            # sys.stdout = redir

            #  Thread starts here to ensure its on the main thread
            t = threading.Thread(target=logicConsoleOutput.follow, name='CONSOLE THREAD', args=(elog, console.log))
            t.start()

class RedirectText(object):

    def __init__(self,TextCtrl):

        self.out=TextCtrl
        self.__line_num = 0

    def line_num(self,reset=False):
        if not reset:
            self.__line_num += 1
            return self.__line_num
        else:
            self.__line_num = 0

    def write(self,string):

        args = string.split('|')
        string = args[-1]
        args = [a.strip() for a in args[:-1]]

        if len(string.strip()) > 0:

            string += '\n'
            if 'RESET' in args:
                self.line_num(reset=True)
                return


            string = str(self.line_num())+ ':  '+string if string != '\n' else string
            self.out.SetInsertionPoint(0)
            if 'WARNING' in args:
                self.out.BeginTextColour((255, 140, 0))
            elif 'ERROR' in args:
                self.out.BeginTextColour((255, 0, 0))
            elif not 'DEBUG' in args:
                self.out.BeginTextColour((0, 0, 0))

            # self.out.Text =  self.out.Text.Insert(string+ "\n");

            self.out.WriteText(string)
            self.out.EndTextColour()

            self.out.Refresh()

    def flush(self):
        pass

class ConsoleTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.log = wx.richtext.RichTextCtrl(self, -1, size=(100,100),
                                            style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.SIMPLE_BORDER|wx.CURSOR_NONE)

        self.log.Bind(wx.EVT_CONTEXT_MENU, self.onRightUp)

        # Add widgets to a sizer
        sizer = wx.BoxSizer()
        sizer.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)

        self.SetSizerAndFit(sizer)

    def onRightUp(self, event):
        self.log.PopupMenu(ConsoleContextMenu(self, event))

class TimeSeriesTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._databases = {}
        self._connection_added = True

        # self.__logger = logging.getLogger('root')


        connection_choices = []
        self.connection_combobox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), connection_choices,
                                             0)
        self.__selected_choice_idx = 0
        self.connection_combobox.SetSelection(self.__selected_choice_idx)

        self.connection_refresh_button = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        self.addConnectionButton = wx.Button(self, wx.ID_ANY, u"Add Connection", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_olvSeries = LogicDatabase(self, pos=wx.DefaultPosition, size=wx.DefaultSize, id=wx.ID_ANY,
                                         style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.m_olvSeries.DefineColumns(self.table_columns)

        # Bindings
        self.addConnectionButton.Bind(wx.EVT_LEFT_DOWN, self.AddConnection)
        self.addConnectionButton.Bind(wx.EVT_MOUSEWHEEL, self.AddConnection_MouseWheel)

        self.connection_refresh_button.Bind(wx.EVT_LEFT_DOWN, self.OLVRefresh)
        self.connection_combobox.Bind(wx.EVT_CHOICE, self.DbChanged)
        # self.connection_combobox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.RefreshComboBox) todo: delete this

        # Sizers
        seriesSelectorSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        #  These two comments below will stack the buttons on the left side of the datatable. For visualization only.
        # seriesSelectorSizer = wx.BoxSizer(wx.HORIZONTAL)
        # buttonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.SetMinSize(wx.Size(-1, 45))

        buttonSizer.Add(self.connection_combobox, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=2)
        buttonSizer.Add(self.addConnectionButton, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        buttonSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        buttonSizer.Add(self.connection_refresh_button, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=2)
        seriesSelectorSizer.Add( buttonSizer, 0, wx.ALL|wx.EXPAND, 0)
        seriesSelectorSizer.Add(self.m_olvSeries, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(seriesSelectorSizer)
        self.Layout()

        # Publisher.subscribe(self.connection_added_status, "connectionAddedStatus")

        engineEvent.onDatabaseConnected += self.refreshConnectionsListBoxTS

        # build custom context menu
        menu = TimeSeriesContextMenu(self.m_olvSeries)
        self.m_olvSeries.setContextMenu(menu)

        # object to hold the current session
        self.__current_session = None

    # def RefreshComboBox(self, event):  # todo: delete this
    #     pass


    def DbChanged(self, event):
        # refresh the database
        self.OLVRefresh(event)

    def refreshConnectionsListBoxTS(self, connection_added):

        if connection_added:
            self._databases = engine.getDbConnections()

            choices = ['---']
            for k, v in self._databases.iteritems():
                choices.append(self._databases[k]['name'])

            for key, value in self.getPossibleConnections().iteritems():
                choices.append(key)

            choices.sort()

            self.connection_combobox.SetItems(choices)


            # set the selected choice
            self.connection_combobox.SetSelection( self.__selected_choice_idx)

    def connection_added_status(self, value=None, connection_string=''):
        if value is not None:
            self._connection_added = value
            self._conection_string = connection_string
        return self._connection_added

    def AddConnection_MouseWheel(self, event):
        '''
        This is intentionally empty to disable mouse scrolling in the AddConnection combobox
        :param event: EVT_MOUSEWHEEL
        :return: None
        '''
        pass

    def AddConnection(self, event):

        params = []

        while 1:
            dlg = AddConnectionDialog(self, -1, "Sample Dialog", size=(350, 200),
                             style=wx.DEFAULT_DIALOG_STYLE,
                             )
            dlg.CenterOnScreen()

            if params:
                dlg.set_values(title=params[0],
                                  desc = params[1],
                                  engine = params[2],
                                  address = params[3],
                                  name = params[4],
                                  user = params[5],
                                  pwd = params[6])

            # this does not return until the dialog is closed.
            val = dlg.ShowModal()


            if val == 5101:
                # cancel is selected
                return
            elif val == 5100:
                params = dlg.getConnectionParams()

                dlg.Destroy()

                # create the database connection
                Publisher.sendMessage('DatabaseConnection',
                                      title=params[0],
                                      desc=params[1],
                                      dbengine=params[2],
                                      address=params[3],
                                      name=params[4],
                                      user=params[5],
                                      pwd=params[6])

                if self.connection_added_status():
                    Publisher.sendMessage('getDatabases')
                    return
                else:

                    wx.MessageBox('I was unable to connect to the database with the information provided :(', 'Info', wx.OK | wx.ICON_ERROR)

    def getPossibleConnections(self):
        wsdl = {}
        wsdl["Red Butte Creek"] = "http://data.iutahepscor.org/RedButteCreekWOF/cuahsi_1_1.asmx?WSDL"
        wsdl["Provo River"] = "http://data.iutahepscor.org/ProvoRiverWOF/cuahsi_1_1.asmx?WSDL"
        wsdl["Logan River"] = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"
        return wsdl

    def prepareODM1_Model(self, siteObject):
        self.selectedVariables = []
        siteview = SiteViewer(self, siteObject)
        siteview.populateVariablesList(self.api, siteObject.sitecode)
        return

    def setParsedValues(self, siteObject):
        # This method will get the values for variables passed.
        values = self.api.parseValues(siteObject.sitecode, self.selectedVariables[0])

        pass

    def setup_odm1_table(self, api):
        data = api.getSiteInfo()
        self.table_columns = ["Site Name", "County", "State"]
        self.m_olvSeries.DefineColumns(self.table_columns)

        output = []
        for da in data:
            d = {
                "site_name": da[0],  # The key MUST match one in the table_columns IN LOWERCASE. FYI
                "county": da[1],
                "state": da[2],
                "sitecode": da[3]
            }

            record_object = type('WOFRecord', (object,), d)
            output.extend([record_object])
        self.m_olvSeries.AutoSizeColumns()
        self.m_olvSeries.SetObjects(output)

    def refresh_database(self):
        # get the name of the selected database
        selected_db = self.connection_combobox.GetStringSelection()

        for key, value in self.getPossibleConnections().iteritems():
            if selected_db == key:
                return value

        self.table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.m_olvSeries.DefineColumns(self.table_columns)

        self.__selected_choice_idx = self.connection_combobox.GetSelection()

        for key, db in self._databases.iteritems():
            # get the database session associated with the selected name
            if db['name'] == selected_db:

                # query the database and get basic series info

                series = None
                # fixme: This breaks for SQLite since it is implemented in dbapi_v2
                if db['args']['engine'] == 'sqlite':
                    import db.dbapi_v2 as db2
                    from ODM2PythonAPI.src.api.ODMconnection import dbconnection
                    session = dbconnection.createConnection(engine=db['args']['engine'], address=db['args']['address'])
                    # gui_utils.connect_to_db()
                    s = db2.connect(session)
                    series = s.getAllSeries()

                else:  # fixme: this is old api for postgresql and mysql (need to update to dbapi_v2)
                    session = dbUtilities.build_session_from_connection_string(db['connection_string'])
                    u = dbapi.utils(session)
                    series = u.getAllSeries()

                if series is None:
                    d = {key: value for (key, value) in
                         zip([col.lower().replace(' ','_') for col in self.table_columns],["" for c in self.table_columns])}
                    record_object = type('DataRecord', (object,), d)
                    data = [record_object]
                else:

                    # loop through all of the returned data
                    data = []
                    for s in series:
                        d = {
                            'resultid': s.ResultID,
                            'variable': s.VariableObj.VariableCode,
                            'unit': s.UnitObj.UnitsName,
                            'date_created': s.FeatureActionObj.ActionObj.BeginDateTime,
                            'type': s.FeatureActionObj.ActionObj.ActionTypeCV,
                            'featurecode': s.FeatureActionObj.SamplingFeatureObj.SamplingFeatureCode,
                            'organization': s.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName
                        }

                        record_object = type('DataRecord', (object,), d)
                        data.extend([record_object])

                # set the data objects in the olv control
                self.m_olvSeries.SetObjects(data)

                # set the current database in canvas controller
                Publisher.sendMessage('SetCurrentDb',value=selected_db)  # sends to CanvasController.getCurrentDbSession

                # fire the onDbChanged Event
                kwargs = dict(dbsession=session,
                              dbname=db['name'],
                              dbid=db['id'])
                events.onDbChanged.fire(**kwargs)
                break

        return

    def OLVRefresh(self, event):
        # if sys.gettrace():
        #     #  In debug mode
        #     self.refresh_database()
        # else:
        #     # Not in debug mode
        #     thr = threading.Thread(target=self.refresh_database, name='DATABASE REFRESH THREAD', args=(), kwargs={})
        #     thr.start()
        value = self.refresh_database()
        if value is not None:
            self.api = WebServiceApi(value)
            self.setup_odm1_table(self.api)



class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(545, 140), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)


class SiteViewer(wx.Frame):
    def __init__(self, parent, siteObject):
        wx.Frame.__init__(self, parent=parent, id=-1, title="Site Viewer", pos=wx.DefaultPosition, size=(650, 700),
                          style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.siteobject = siteObject
        self.startDate = wx.DateTime_Now() - 7 * wx.DateSpan_Day()
        self.endDate = wx.DateTime_Now()
        self.parent = parent

        panel = wx.Panel(self)
        self.toppanel = wx.Panel(panel)
        middlepanel = wx.Panel(panel, size=(-1, 35))
        secondMiddle = wx.Panel(panel, size=(-1, 35))
        lowerpanel = wx.Panel(panel)

        #  Uncomment these to see the panel outline
        # toppanel.SetBackgroundColour("#AAFFCC")
        # middlepanel.SetBackgroundColour("#00FF00")
        # lowerpanel.SetBackgroundColour("#FF00FF")

        hboxTopPanel = wx.BoxSizer(wx.HORIZONTAL)

        plot = self.loadEmptyGraph(self.toppanel)

        hboxTopPanel.Add(plot.plot, 1, wx.EXPAND | wx.ALL, 2)

        self.toppanel.SetSizer(hboxTopPanel)


        hboxMidPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.startDateBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Start Date")
        self.endDateBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="End Date")
        self.exportBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Export")
        self.addToCanvasBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Add to Canvas")
        self.PlotBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Plot Panel")

        hboxMidPanel.Add(self.startDateBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(20)
        hboxMidPanel.Add(self.endDateBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(20)
        hboxMidPanel.Add(self.exportBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(20)
        hboxMidPanel.Add(self.addToCanvasBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(20)
        hboxMidPanel.Add(self.PlotBtn, 1, wx.EXPAND | wx.ALL, 2)
        middlepanel.SetSizer(hboxMidPanel)

        hboxLowPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Column names
        self.variableList = CheckListCtrl(lowerpanel)
        self.variableList.InsertColumn(0, "Variable")
        self.variableList.InsertColumn(1, "Value")
        self.variableList.InsertColumn(2, "Unit")

        hboxLowPanel.Add(self.variableList, 1, wx.EXPAND | wx.ALL, 2)
        lowerpanel.SetSizer(hboxLowPanel)
        #self.startDateText = wx.StaticText(self, -1, "Start Date: " + self.startDate.__str__())

        #mhbox = wx.BoxSizer(wx.HORIZONTAL)
        #mhbox.Add(self.startDateText, 1, wx.EXPAND | wx.ALL, 2)
        #secondMiddle.SetSizer(mhbox)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(self.toppanel, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(middlepanel, 0, wx.EXPAND | wx.ALL, 2)
        #vbox.Add(secondMiddle, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(lowerpanel, 1, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.Plot, self.PlotBtn)
        self.Bind(wx.EVT_BUTTON, self.startDateCalender, self.startDateBtn)
        self.Bind(wx.EVT_BUTTON, self.endDateCalender, self.endDateBtn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, id=self.addToCanvasBtn.GetId())
        self.isCalendarOpen = False  # Used to prevent calendar being open twice

        self.Show()

    def addToCanvas(self, event):
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsChecked(i):
                self.Parent.selectedVariables.append(self.variableList.GetItemText(i))

        self.Close()
        if len(self.Parent.selectedVariables) > 1:
            self.Parent.setParsedValues(self.siteobject)

    def endDateCalender(self, event):
        if self.isCalendarOpen:
            pass
        else:
            Calendar(self, -1, "Calendar", "end")

    def loadEmptyGraph(self, panel):
        p = ViewPlotForSiteViewer(panel)
        return p

    def Plot(self, event):
        #  TODO: make this plot data
        plotting = ViewPlot(parent=self, title="Should auto fill", selector=False)
        plotting.Show()
        print "test"

    def populateVariablesList(self, api, sitecode):
        data = api.buildAllSiteCodeVariables(sitecode)
        count = 0
        for key, value, in data.iteritems():
            pos = self.variableList.InsertStringItem(count, str(key))
            self.variableList.SetStringItem(pos, 1, value)
            count += 1

        # Auto size column
        self.variableList.setResizeColumn(0)
        self.variableList.setResizeColumn(1)
        self.variableList.setResizeColumn(2)

    def startDateCalender(self, event):
        if self.isCalendarOpen:
            pass
        else:
            Calendar(self, -1, "Calendar", "start")

class Calendar(wx.Dialog):
    def __init__(self, parent, id, title, type):
        wx.Dialog.__init__(self, parent, id, title, style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^
                                                                           wx.MAXIMIZE_BOX)
        self.type = type

        self.Parent.isCalendarOpen = True

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.calendar = cal.CalendarCtrl(self, -1, wx.DateTime_Now(),
                                  style=cal.CAL_SHOW_HOLIDAYS | cal.CAL_SEQUENTIAL_MONTH_SELECTION)
        vbox.Add(self.calendar, 0, wx.EXPAND | wx.ALL, 5)

        vbox.Add((-1, 20))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(self, -1, 'Date')
        hbox.Add(self.text)
        vbox.Add(hbox, 0, wx.LEFT, 8)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, -1, 'Ok')
        hbox2.Add(btn, 1)
        vbox.Add(hbox2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.Bind(wx.EVT_BUTTON, self.OnQuit, id=btn.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.SetSizerAndFit(vbox)

        self.Show(True)
        self.Centre()

    def OnQuit(self, event):
        self.setCalendarDates()
        if self.validateDates():
            self.Parent.isCalendarOpen = False
            self.Destroy()
        else:
            self.text.SetLabel("Make start before end")

    def setCalendarDates(self):
        if self.type == "start":
            self.Parent.startDate = self.calendar.GetDate()
            self.Parent.startDateBtn.SetLabelText(self.calendar.GetDate().FormatDate())
        else:
            self.Parent.endDate = self.calendar.GetDate()
            self.Parent.endDateBtn.SetLabelText(self.calendar.GetDate().FormatDate())

    def validateDates(self):
        if self.Parent.startDate < self.Parent.endDate:
            print "Start is before End So its GOOD "
            return True
        else:
            print "Please fix, make start before END, FAIL"
            return False


class AddConnectionDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,
            ):

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        self.PostCreate(pre)

        gridsizer = wx.FlexGridSizer(rows=7,cols=2,hgap=5,vgap=5)

        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Database Connection")
        titleSizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        ######################################################

        label = wx.StaticText(self, -1, "*Title :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Title of the database connection")
        self.title = wx.TextCtrl(self, wx.ID_ANY, '', size=(200,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.title, 0, wx.EXPAND)


        label = wx.StaticText(self, -1, "Description :")
        label.SetHelpText("Description of the database connection")
        self.description = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.description, 0, wx.EXPAND)

        ######################################################


        label = wx.StaticText(self, -1, "*Engine :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Database Parsing Engine (e.g. mysql, psycopg2, etc)")
        #self.engine = wx.TextCtrl(self, -1, "", size=(80,-1))
        engine_choices = ['PostgreSQL', 'MySQL']
        self.engine = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, engine_choices, 0 )
        self.engine.SetSelection( 0 )
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.engine, 0, wx.EXPAND)


        label = wx.StaticText(self, -1, "*Address :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Database Address")
        self.address = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.address, 0, wx.EXPAND)

        label = wx.StaticText(self, -1, "*Database :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Database Name")
        self.name = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.name, 0, wx.EXPAND)

        label = wx.StaticText(self, -1, "*User :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Database Username")
        self.user = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.user, 0, wx.EXPAND)

        label = wx.StaticText(self, -1, "Password :")
        label.SetHelpText("Database Password")
        self.password = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.password, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(titleSizer, 0, wx.CENTER)
        sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(gridsizer, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizeHints(250, 300, 500, 400)


        btnsizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)

        self.btnok = wx.Button(self, wx.ID_OK)
        self.btnok.SetDefault()
        btnsizer.AddButton(self.btnok)
        self.btnok.Disable()

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


        #self.engine.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.address.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.name.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.user.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.title.Bind(wx.EVT_TEXT, self.OnTextEnter)


    def set_values(self,title,desc,engine, address, name, user,pwd):
        self.title.Value = title
        self.description.Value = desc
        self.engine.Value = engine
        self.address.Value = address
        self.name.Value = name
        self.user.Value = user
        self.password.Value = pwd

    def getConnectionParams(self):

        engine = self.engine.GetStringSelection().lower()

        #engine = self.engine.GetValue()
        address = self.address.GetValue()
        name = self.name.GetValue()
        user = self.user.GetValue()
        pwd = self.password.GetValue()
        title = self.title.GetValue()
        desc = self.description.GetValue()

        return title,desc, engine,address,name,user,pwd,title,desc

    def OnTextEnter(self, event):
        if self.address.GetValue() == '' or  \
                self.name.GetValue() == '' or  \
                self.user.GetValue() == '' or \
                self.title.GetValue() == '':
            self.btnok.Disable()
        else:
            self.btnok.Enable()

class DataSeries(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 500),
                          style=wx.TAB_TRAVERSAL)

        self._databases = {}
        self._connection_added = True

        connection_choices = []
        self.connection_combobox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), connection_choices,
                                             0)
        self.__selected_choice_idx = 0
        self.connection_combobox.SetSelection(0)

        self.connection_refresh_button = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        self.addConnectionButton = wx.Button(self, wx.ID_ANY, u"Add Connection", wx.DefaultPosition, wx.DefaultSize, 0)

        self.table = LogicDatabase(self, pos=wx.DefaultPosition, size=wx.DefaultSize, id=wx.ID_ANY,
                                   style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        # Bindings
        self.addConnectionButton.Bind(wx.EVT_LEFT_DOWN, self.AddConnection)
        self.addConnectionButton.Bind(wx.EVT_MOUSEWHEEL, self.AddConnection_MouseWheel)

        self.connection_refresh_button.Bind(wx.EVT_LEFT_DOWN, self.database_refresh)
        self.connection_combobox.Bind(wx.EVT_CHOICE, self.DbChanged)

        # Sizers
        seriesSelectorSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.SetMinSize(wx.Size(-1, 45))

        buttonSizer.Add(self.connection_combobox, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=2)
        buttonSizer.Add(self.addConnectionButton, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        buttonSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        buttonSizer.Add(self.connection_refresh_button, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=2)
        seriesSelectorSizer.Add( buttonSizer, 0, wx.ALL|wx.EXPAND, 0)
        seriesSelectorSizer.Add(self.table, 1, wx.ALL|wx.EXPAND, 0)

        self.SetSizer(seriesSelectorSizer)
        self.Layout()

        #databases = Publisher.sendMessage('getDatabases')
        # Publisher.subscribe(self.getKnownDatabases, "getKnownDatabases")  # sends message to CanvasController
        # Publisher.subscribe(self.connection_added_status, "connectionAddedStatus")
        engineEvent.onDatabaseConnected += self.refreshConnectionsListBox

    def DbChanged(self, event):
        self.database_refresh(event)

    def refreshConnectionsListBox(self, connection_added):

        if connection_added:
            self._databases = engine.getDbConnections()

            choices = ['---']
            for k, v in self._databases.iteritems():
                choices.append(self._databases[k]['name'])
            self.connection_combobox.SetItems(choices)

            # set the selected choice
            self.connection_combobox.SetSelection( self.__selected_choice_idx)

    def connection_added_status(self,value=None,connection_string=''):
        if value is not None:
            self._connection_added = value
            self._connection_string = connection_string
        return self._connection_added

    def AddConnection_MouseWheel(self, event):
        '''
        This is intentionally empty to disable mouse scrolling in the AddConnection combobox
        :param event: EVT_MOUSEWHEEL
        :return: None
        '''
        pass

    def AddConnection(self, event):

        params = []

        while 1:
            dlg = AddConnectionDialog(self, -1, "Sample Dialog", size=(350, 200),
                             style=wx.DEFAULT_DIALOG_STYLE,
                             )
            dlg.CenterOnScreen()

            if params:
                dlg.set_values(title=params[0],
                                  desc=params[1],
                                  engine=params[2],
                                  address=params[3],
                                  name=params[4],
                                  user=params[5],
                                  pwd=params[6])

            # this does not return until the dialog is closed.
            val = dlg.ShowModal()


            if val == 5101:
                # cancel is selected
                return
            elif val == 5100:
                params = dlg.getConnectionParams()

                dlg.Destroy()

                # create the database connection
                Publisher.sendMessage('DatabaseConnection',
                                      title=params[0],
                                      desc = params[1],
                                      engine = params[2],
                                      address = params[3],
                                      name = params[4],
                                      user = params[5],
                                      pwd = params[6])

                if self.connection_added_status():
                    Publisher.sendMessage('getDatabases')
                    return
                else:

                    wx.MessageBox('I was unable to connect to the database with the information provided :(', 'Info', wx.OK | wx.ICON_ERROR)

    def load_data(self):
        elog.error('Abstract method. Must be overridden!')
        raise Exception('Abstract method. Must be overridden!')

    def database_refresh(self, event):
        if sys.gettrace():
            #  In debug mode
            self.load_data()
        else:
            # Not in debug mode
            thr = threading.Thread(target=self.load_data, args=(), kwargs={}, name='DataSeriesRefresh')
            thr.start()

class SimulationDataTab(DataSeries):
    def __init__(self, parent):
        #  wx.Panel.__init__(self, parent)

        super(SimulationDataTab, self).__init__(parent)
        self.parent = parent

        self.table_columns = ["Simulation ID", "Simulation Name", "Model Name", "Simulation Start", "Simulation End", "Date Created","Owner"]
        #  table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.table.DefineColumns(self.table_columns)

        self.__selected_choice_idx = 0

        # build custom context menu
        menu = SimulationContextMenu(self.table)
        self.table.setContextMenu(menu)
        self.conn = None

    def load_data(self):

        # get the name of the selected database
        selected_db = self.connection_combobox.GetStringSelection()

        #set the selected choice
        self.__selected_choice_idx = self.connection_combobox.GetSelection()

        for key, db in self._databases.iteritems():        # # deactivate the console if we are in debug mode
            # if not sys.gettrace():
            #     redir = RedirectText(self.log)
            #     sys.stdout = redir

            # get the database session associated with the selected name
            isSqlite = False

            if db['name'] == selected_db:
                simulations = None

                if db['args']['engine'] == 'sqlite':
                    import db.dbapi_v2 as db2
                    from ODM2PythonAPI.src.api.ODMconnection import dbconnection
                    session = dbconnection.createConnection(engine=db['args']['engine'], address=db['args']['address'])
                    self.conn = db2.connect(session)
                    simulations = self.conn.getAllSimulations()
                    isSqlite = True
                    self.conn.getCurrentSession()
                else:
                    session = dbUtilities.build_session_from_connection_string(db['connection_string'])
                    # build the database session

                    u = dbapi.utils(session)
                    simulations = u.getAllSimulations()


                #     # gui_utils.connect_to_db()
                #
                #
                # else: # fixme: this is old api for postgresql and mysql (need to update to dbapi_v2)
                #     session = dbUtilities.build_session_from_connection_string(db['connection_string'])
                #     u = dbapi.utils(session)
                #     series = u.getAllSeries()


                sim_ids = []
                if simulations is None:
                    d = {key: value for (key, value) in
                         zip([col.lower().replace(' ','_') for col in self.table_columns],["" for c in self.table_columns])}
                    record_object = type('DataRecord', (object,), d)
                    data = [record_object]
                else:
                    data = []

                    # loop through all of the returned data

                    for s in simulations:
                        simulation = None
                        if isSqlite:
                            simulation = s.Simulations
                            person = s.People
                            action = s.Actions
                            model = s.Models
                        else:
                            simulation = s.Simulation
                            person = s.Person
                            action = s.Action
                            model = s.Model

                        simulation_id = simulation.SimulationID

                        # only add if the simulation id doesn't already exist in sim_ids
                        if simulation_id not in sim_ids:
                            sim_ids.append(simulation_id)

                            d = {
                                'simulation_id': simulation.SimulationID,
                                'simulation_name': simulation.SimulationName,
                                'model_name': model.ModelName,
                                'date_created': action.BeginDateTime,
                                'owner': person.PersonLastName,
                                'simulation_start': simulation.SimulationStartDateTime,
                                'simulation_end': simulation.SimulationEndDateTime,
                                'model_id': simulation.ModelID
                            }

                            record_object = type('DataRecord', (object,), d)
                            data.extend([record_object])

                # set the data objects in the olv control
                self.table.SetObjects(data)

                # set the current database in canvas controller
                Publisher.sendMessage('SetCurrentDb', value=selected_db)  # sends to CanvasController.getCurrentDbSession
