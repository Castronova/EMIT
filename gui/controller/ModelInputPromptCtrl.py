from gui.views.ModelInputPromptView import ModelInputPromptView
import wx


class ModelInputPromptCtrl(ModelInputPromptView):
    def __init__(self, parent, path):
        ModelInputPromptView.__init__(self, parent, path)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    ####################################
    # EVENTS
    ####################################

    def on_close(self, event):
        self.MakeModal(False)
        self.Destroy()
