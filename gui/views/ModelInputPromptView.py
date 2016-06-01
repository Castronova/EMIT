from utilities import models
import wx


class ModelInputPromptView(wx.Frame):
    def __init__(self, parent, path):
        wx.Frame.__init__(self, parent, title="Input Prompt", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)

        panel = wx.Panel(self)
        data = models.parse_json(path)

        if "model_inputs" not in data:
            print "Data does not have 'model_inputs' as key"
            return

        model_inputs = data["model_inputs"]
        count = 0  # Keeps track of how many input items there are
        self.static_texts = []
        self.text_ctrls = []
        self.help_texts = []
        self.inputs = []

        # Add components dynamically
        for item in model_inputs:
            static_text = wx.StaticText(panel, id=count, label=item["label"] + ":")
            text_ctrl = wx.TextCtrl(panel, id=count)
            help_text = wx.StaticText(panel, id=count, label=item["help"])
            file_explorer_button = None
            if item["input"] == "file":
                file_explorer_button = wx.Button(panel, id=count, label="File", style=wx.BU_EXACTFIT)

            font = wx.Font(pointSize=8, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)
            help_text.SetFont(font)

            # Keep track of all the components in the lists
            self.static_texts.append(static_text)
            self.text_ctrls.append(text_ctrl)
            self.inputs.append(file_explorer_button)
            self.help_texts.append(help_text)
            count += 1

        break_line = wx.StaticLine(panel)
        self.submit_button = wx.Button(panel, label="Submit", style=wx.BU_EXACTFIT)

        # Create sizers
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        flex_grid_sizer = wx.FlexGridSizer(rows=count * 2, cols=3, vgap=1, hgap=5)

        # Add components to sizer
        for i in range(count):
            flex_grid_sizer.Add(self.static_texts[i])
            flex_grid_sizer.Add(self.text_ctrls[i], 1, wx.EXPAND)
            if self.inputs[i]:
                flex_grid_sizer.Add(self.inputs[i])
            else:
                flex_grid_sizer.AddSpacer((0, 0))

            flex_grid_sizer.AddSpacer((0, 0))
            flex_grid_sizer.Add(self.help_texts[i], 1, wx.EXPAND | wx.BOTTOM, 10)
            flex_grid_sizer.AddSpacer((0, 0))

        flex_grid_sizer.AddGrowableCol(1, 1)  # Set the second column to expand and fill space

        frame_sizer.Add(flex_grid_sizer, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        frame_sizer.Add(break_line, 0, wx.EXPAND, 5)
        frame_sizer.Add(self.submit_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        panel.SetSizer(frame_sizer)
        frame_sizer.Fit(self)

        self.Show()
        # Disables all other windows in the application so that the user can only interact with this window.
        self.MakeModal(True)
