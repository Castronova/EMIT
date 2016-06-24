from gui.views.ModelInputPromptView import ModelInputPromptView
import wx
from sprint import *
from utilities.models import *
import __builtin__
from gui.Models.MarkdownWindow import MarkdownWindow


class ModelInputPromptCtrl(ModelInputPromptView):
    def __init__(self, parent, path):
        ModelInputPromptView.__init__(self, parent, path)

        # exit if parameters are invalid
        if not self.valid_params:
            return

        self.mdl_path = path
        self.emitCtrl = parent


        # load the model or simulation with the parsed parameters only since no additional inputs are needed
        if not self.has_inputs:
            if self.params['type'] == 'mdl':
                self.emitCtrl.Canvas.addModel(**self.params)
            else:
                self.emitCtrl.Canvas.load_simulation(path)
            return

        # Disables all other windows in the application so that the user can only interact with this window.
        self.MakeModal(True)

        # Bindings
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_close)
        self.help_button.Bind(wx.EVT_BUTTON, self.on_help)
        for button in self.inputs:
            if button:
                button.Bind(wx.EVT_BUTTON, self.on_file_browser)

    ####################################
    # EVENTS
    ####################################

    def on_close(self, event):
        self.MakeModal(False)
        self.Destroy()

    def on_file_browser(self, event):
        file_browser = wx.FileDialog(self, message="Load file")
        if file_browser.ShowModal() == wx.ID_OK:
            self.text_ctrls[event.GetId()].SetValue(file_browser.GetPath())

    def on_help(self, event):
        print "Show markdown"
        MarkdownWindow(self)


    def on_submit(self, event):

        if validate_json_model(self.params):

            try:
                # loop through the dynamically created user inputs and put into params dictionary
                for i in range(0, len(self.variable_names)):
                    if self.text_ctrls[i].Value == '':
                        if self.required:
                            raise Exception('Required field not provided [%s]' % self.variable_names[i])
                        self.params[self.variable_names[i]] = None
                    else:
                        self.params[self.variable_names[i]] = getattr(__builtin__, self.variable_types[i])(self.text_ctrls[i].Value)

                # load the model with these parsed and formatted parameters
                self.emitCtrl.Canvas.addModel(**self.params)

            except Exception as e:
                msg = 'Encountered and error when parsing MDL datatypes: %s' % e
                sPrint(msg, MessageType.ERROR)


        else:
            sPrint('Could not load model, input parameters are invalid', MessageType.ERROR)

        # close the window
        self.on_close(event)

