#Boa:Wizard:wizSave

import wx
import wx.wizard as wiz

# import * from WizardPanels
# import pnlMethod
# import pnlQCL
# import pnlVariable
# import pnlSummary
import pnlCreateLink
import pnlSpatial
import pnlTemporal
import pnlDetails
import pnlSummary
import PropertyGrid
from wx.lib.pubsub import pub as Publisher
from utilities.gui import *


[wxID_WIZLINK, wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
] = [wx.NewId() for _init_ctrls in range(5)]

from wx.lib.pubsub import pub as Publisher
#from common.logger import LoggerTool
import logging
#tool = LoggerTool()
#logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

######################################################################

class Details(wiz.PyWizardPage):
    def __init__(self, parent, title, inputitems, outputitems):
        """Constructor"""
        wiz.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)


        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        # self.pnlDetail=pnlSummary.pnlDetails(self)

        #from_model = parent.cmd.

        self.pnlDetail=pnlSummary.TestPanel(self, inputitems, outputitems)
        self.sizer.Add(self.pnlDetail, 85, wx.ALL, 5)


    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return

    def GetPrev(self):
        return self.prev

######################################################################

class Temporal(wiz.PyWizardPage):
    def __init__(self, parent, title):
        """Constructor"""
        wiz.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.pnlIntroduction=pnlTemporal.pnlTemporal(self)
        self.sizer.Add(self.pnlIntroduction, 85, wx.ALL, 5)

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev

######################################################################

class Spatial(wiz.PyWizardPage):
    def __init__(self, parent, title):
        """Constructor"""
        wiz.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.pnlIntroduction=pnlSpatial.pnlSpatial(self)
        self.sizer.Add(self.pnlIntroduction, 85, wx.ALL|wx.EXPAND, 5)

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev

#######################################################################

class CreateLink(wiz.PyWizardPage):
    def __init__(self, parent, title, from_model_name, to_model_name, inputitems, outputitems):
        """Constructor"""
        wiz.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.pnlIntroduction=pnlCreateLink.pnlCreateLink(self, from_model_name, to_model_name, inputitems, outputitems)
        self.sizer.Add(self.pnlIntroduction, 85, wx.ALL, 5)




    def GetName(*args, **kwargs):
        return 'CreateLink'

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):

        return self.next


    def GetPrev(self):
        return self.prev


########################################################################

class TitledPage(wiz.WizardPageSimple):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, title):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)


########################################################################
class wizLink(wx.wizard.Wizard):
    def _init_ctrls(self, parent):
        # generated method, don't edit
        wiz.Wizard.__init__(self, parent, id=wxID_WIZLINK,
               title=u'Link Creation Wizard')
        self.SetToolTipString(u'Add Link')
        self.SetName(u'wizLink')
##self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onPlotSelection, id=wxID_RIBBONPLOTTIMESERIES)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_page_changing)
        self.Bind(wx.wizard.EVT_WIZARD_FINISHED, self.on_wizard_finished)

        self.initSubscribers()


    def initSubscribers(self):
        Publisher.subscribe(self.activateNextButton, "activateNextButton")
        Publisher.subscribe(self.deactivateNextButton, "deactivateNextButton")

    def activateNextButton(self):
        foward_btn = self.FindWindowById(wx.ID_FORWARD)
        foward_btn.Enable()

    def deactivateNextButton(self):
        foward_btn = self.FindWindowById(wx.ID_FORWARD)
        foward_btn.Disable()

    def get_metadata(self):
        pass
        # if self.is_changing_series:
        #     method = self.page2.panel.getMethod()
        #     qcl = self.page3.panel.getQCL()
        #     variable = self.page4.panel.getVariable()
        # else:
        #     method = self.currSeries.method
        #     qcl = self.currSeries.quality_control_level
        #     variable =self.currSeries.variable
        # site = self.currSeries.site
        # source = self.currSeries.source
        # #logger.debug("site: %s, variable: %s, method: %s, source: %s, qcl: %s"% (site.id,variable.id, method.id, source.id, qcl.id))
        # return site, variable, method, source, qcl

    def __init__(self, parent, outputid, inputid, outputitems, inputitems, cmd):
        self._init_ctrls(parent)
        #self.series_service = service_man.get_series_service()
        #self.record_service = record_service
        self.is_changing_series = False
        #self.currSeries = record_service.get_series()
        self.cmd = cmd
        self.inputid = inputid
        self.outputid = outputid

        input_model_name = cmd.get_model_by_id(inputid).get_name()
        output_model_name = cmd.get_model_by_id(outputid).get_name()
        self.page1 = CreateLink(self, "Add Link", output_model_name, input_model_name, inputitems, outputitems)

        self.page2 = Spatial(self, "Spatial Adjustment")
        self.page3 = Temporal(self, "Temporal Adjustment")
        self.page4 = Details(self, "Link Details", inputitems, outputitems)
        #self.page5 = SummaryPage(self, "Summary", service_man)

        self.FitToPage(self.page1)
##        page5.sizer.Add(wx.StaticText(page5, -1, "\nThis is the last page."))

        # Set the initial order of the pages
        # self.page1.SetNext(self.page2)
        # self.page2.SetNext(self.page3)
        self.page1.SetNext(self.page4)

       #
        self.page4.SetPrev(self.page1)
        # self.page3.SetPrev(self.page2)
        # self.page4.SetPrev(self.page3)
        # self.page4.SetNext(self.page5)
        #
        # self.page5.SetPrev(self.page4)

##        fin_btn = self.FindWindowById(wx.ID_FINISH)
##        fin_btn.SetLabel("Save Series")
        self.GetPageAreaSizer().Add(self.page1)
        self.RunWizard(self.page1)
        self.Destroy()

    def on_page_changing(self, event):

        if event.Page.GetName() == "CreateLink":
            pass


            #self.text3.SetValue(self.text2.GetValue())
        if event.Page == self.page4:
            #print 'here'

            input = self.page1.pnlIntroduction.pgin
            output = self.page1.pnlIntroduction.pgout

            self.page4.pnlDetail.PropGridPopulate(input, output)

            #print self.page1

        if event.Page == self.page3:

            #self.page3.pnlDetail.SetData(self.page1.pnlIntroduction.links)
            self.page4.pnlDetail.SetData(self.page1.pnlIntroduction.get_link())
            self.page4.pnlDetail.printData()

        # elif event.Page==self.page1:
        #     self.is_changing_series = False
        # else:
        #     self.is_changing_series = True


    def on_wizard_finished(self, event):


        #--- create link objects ---

        # get links from page1
        link = self.page1.pnlIntroduction.links

        # set these links in the cmd

        self.cmd.add_link(self.outputid, link[0].name(),
                          self.inputid, link[1].name())


        self.Close()
        event.Skip()




        # Site, Variable, Method, Source, QCL= self.get_metadata()
        # #if qcl exits use its its
        # closeSuccessful = False
        # if QCL.id == 0:
        #     val = wx.MessageBox("You are overwriting an level 0 dataset, which is usually reserved for raw data.\n"
        #                         "Are you sure you want to save?",
        #                         'Are you Sure?',
        #                         wx.YES_NO | wx.ICON_QUESTION)
        #     if val == 2:
        #         #logger.debug("user selected yes to save a level 0 dataset")
        #         val_2 = wx.MessageBox("This action cannot be undone.\nAre you sure, you are sure?\n",
        #                               'Are you REALLY sure?',
        #                               wx.YES_NO | wx.ICON_QUESTION)
        #         if val_2 ==2:
        #             closeSuccessful =True
        #
        # else:
        #     closeSuccessful = True
        #
        #
        #
        #
        # #if QCL.code == 0:
        # #     #TODO MessageBox "you are overwriting an level 0 dataset, which is usually reserved for raw data
        # #     #  are you sure you want to save?"
        # #     val = wx.MessageBox('Are you Sure?', "you are overwriting an level 0 dataset, which is usually reserved"
        # #                                               " for raw data are you sure you want to save?",  wx.YES_NO | wx.ICON_INFORMATION)
        # #
        # #     if val == wx.OK:
        # #         #TODO Message Box "this action cannot be changed are you sure, you are sure you want to save?"
        # #         val2 = wx.MessageBox('Are you Sure?',"this action cannot be changed are you sure, you are sure "
        # #                                                  "you want to save?",  wx.YES_NO | wx.ICON_INFORMATION)
        # #         if val2 != wx.OK:
        # #closeSuccessful = False
        # #             break
        # #     else: closeSuccessful = False
        #
        #
        # if closeSuccessful:
        #     if self.series_service.qcl_exists(QCL):
        #         if QCL==self.currSeries.quality_control_level:
        #             QCL=None
        #         else:
        #             QCL = self.record_service.get_qcl(QCL)
        #     else:
        #         QCL=self.record_service.create_qcl(QCL.code, QCL.definition, QCL.explanation)
        #
        #     #if variable exists use its id
        #     if self.series_service.variable_exists(Variable):
        #         if Variable==self.currSeries.variable:
        #             Variable= None
        #         else:
        #             Variable = self.record_service.get_variable(Variable)
        #     else:
        #         Variable=self.record_service.create_variable(Variable)
        #     #if method exists use its id
        #     if self.series_service.method_exists(Method):
        #         if Method==self.currSeries.method:
        #             Method=None
        #         else:
        #             Method = self.record_service.get_method(Method)
        #     else:
        #         Method=self.record_service.create_method(Method)
        #
        #     # initiate either "Save as" or "Save"
        #     if self.page1.pnlIntroduction.rbSave.GetValue():
        #         result = self.record_service.save(Variable, Method, QCL, False)
        #     else:
        #         result = self.record_service.save(Variable, Method, QCL, True)
        #
        #     if not result:
        #         wx.MessageBox("Save was unsuccessful", "Error!", wx.ICON_ERROR | wx.ICON_EXCLAMATION)
        #     else:
        #         Publisher.sendMessage("refreshSeries")

