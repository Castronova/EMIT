from gui.views.ModelInputPromptView import ModelInputPromptView
import wx


class ModelInputPromptCtrl(ModelInputPromptView):
    def __init__(self, parent, path):
        ModelInputPromptView.__init__(self, parent, path)

        # Bindings
        self.Bind(wx.EVT_CLOSE, self.on_close)
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
