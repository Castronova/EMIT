from utilities import models
import wx


class ModelInputPromptView(wx.Frame):
    def __init__(self, parent, path):
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)

        panel = wx.Panel(self)
        data = models.parse_json(path)

        if "model_inputs" not in data:
            print "Data does not have 'model_inputs' as key"
            return

        title = "Input for " + data["model"][0]["code"]
        self.SetTitle(title)

        model_inputs = data["model_inputs"]
        count = 0  # Keeps track of how many input items there are
        self.static_texts = []
        self.text_ctrls = []
        self.help_texts = []
        self.inputs = []

        # Add components dynamically
        for item in model_inputs:
            static_text = wx.StaticText(panel, id=count, label=item["label"] + ":")
            help_text = wx.StaticText(panel, id=count, label=item["help"])
            text_ctrl = wx.TextCtrl(panel, id=count)

            file_explorer_button = None
            if item["input"] == "file":
                file_explorer_button = wx.Button(panel, id=count, label="Browse", style=wx.BU_EXACTFIT)

            font = wx.Font(pointSize=8, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)
            help_text.SetFont(font)

            # Keep track of all the components in the lists
            self.static_texts.append(static_text)
            self.text_ctrls.append(text_ctrl)
            self.inputs.append(file_explorer_button)
            self.help_texts.append(help_text)
            count += 1

        break_line = wx.StaticLine(panel)
        self.submit_button = wx.Button(panel, label="Load Model", style=wx.BU_EXACTFIT)

        # Create sizers
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        flex_grid_sizer = wx.FlexGridSizer(rows=count * 3, cols=1, vgap=1, hgap=5)

        # Add components to sizer
        for i in range(count):
            # Used to act as if there were two columns. Allows the text ctrl to overflow into the second column
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            word_wrap_sizer = wx.BoxSizer(wx.HORIZONTAL)  # For wrapping the help text

            flex_grid_sizer.Add(self.static_texts[i])

            sizer.Add(self.text_ctrls[i], 1, wx.EXPAND)
            if self.inputs[i]:
                sizer.Add(self.inputs[i], 0, wx.EXPAND)

            flex_grid_sizer.Add(sizer, 1, wx.EXPAND)
            word_wrap_sizer.Add(self.help_texts[i], 1, wx.EXPAND)
            flex_grid_sizer.Add(word_wrap_sizer, 1, wx.EXPAND | wx.BOTTOM, 15)
            flex_grid_sizer.AddGrowableRow(((i + 1) * 3) - 1, 1)

        flex_grid_sizer.AddGrowableCol(0, 1)  # Set the first column to expand and fill space

        frame_sizer.Add(flex_grid_sizer, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        frame_sizer.Add(break_line, 0, wx.EXPAND, 5)
        frame_sizer.Add(self.submit_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        panel.SetSizer(frame_sizer)
        frame_sizer.Fit(self)
        self.SetSize((300, -1))

        self.Show()
        # Disables all other windows in the application so that the user can only interact with this window.
        self.MakeModal(True)
