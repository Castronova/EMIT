from utilities import models
import wx
from sprint import *
import wx.lib.scrolledpanel


class ModelInputPromptView(wx.Frame):
    def __init__(self, parent, path):
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)

        # Create panels
        panel = wx.Panel(self)
        scroll_panel = wx.lib.scrolledpanel.ScrolledPanel(panel)
        scroll_panel.SetupScrolling(scroll_x=False)  # Disable scrolling horizontally
        bottom_panel = wx.Panel(panel)

        self.params = models.parse_json(path)
        self.params.update({'path':path,
                            'type':path[-3:]})

        self.valid_params = 1
        self.has_inputs = 1 if 'model_inputs' in self.params else 0

        # if a sim file is being loaded return, else proceed
        if not self.has_inputs:
            return
        if self.params['type'] == 'sim':
            return
        elif self.params['type'] == 'mdl':
            if not models.validate_json_model(self.params):
                sPrint('Encountered and error when validating parameters: %s' %path)
                self.valid_params = 0  # set the parameter validation as True
                return

        title = "Input for " + self.params["model"][0]["code"]
        self.SetTitle(title)

        model_inputs = self.params["model_inputs"]
        count = 0  # Keeps track of how many input items there are
        self.static_texts = []
        self.text_ctrls = []
        self.help_texts = []
        self.inputs = []
        self.variable_names = []
        self.variable_types = []
        self.required = []

        # Add components dynamically
        for item in model_inputs:
            static_text = wx.StaticText(scroll_panel, id=count, label=item["name"] + ":")
            help_text = wx.StaticText(scroll_panel, id=count, label=item["help"])
            text_ctrl = wx.TextCtrl(scroll_panel, id=count)

            file_explorer_button = None
            if item["input"] == "file":
                file_explorer_button = wx.Button(scroll_panel, id=count, label="Browse", style=wx.BU_EXACTFIT)

            font = wx.Font(pointSize=8, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)
            help_text.SetFont(font)

            # set default values
            if 'default' in item:
                text_ctrl.Value = str(item['default'])

            # save variable types
            if 'datatype' in item:
                self.variable_types.append(item['datatype'])
            else:
                self.variable_types.append('str')

            # Keep track of all the components in the lists
            self.static_texts.append(static_text)
            self.text_ctrls.append(text_ctrl)
            self.inputs.append(file_explorer_button)
            self.help_texts.append(help_text)
            self.variable_names.append(item['variable'])
            self.required.append(bool(item['required']) if 'required' in item else False)
            count += 1

        break_line = wx.StaticLine(panel)
        self.cancel_button = wx.Button(bottom_panel, label="Cancel", style=wx.BU_EXACTFIT)
        self.submit_button = wx.Button(bottom_panel, label="Load Model", style=wx.BU_EXACTFIT)
        self.help_button = wx.Button(bottom_panel, label="Help", style=wx.BU_EXACTFIT)

        # Create sizers
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        scroll_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        flex_grid_sizer = wx.FlexGridSizer(rows=count * 3, cols=1, vgap=1, hgap=5)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

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

        # Adding the flex grid sizer to scroll panel sizer to give margin to the side of the scroll bar
        scroll_panel_sizer.Add(flex_grid_sizer, 1, wx.ALL | wx.EXPAND, 20)
        scroll_panel.SetSizer(scroll_panel_sizer)
        scroll_panel_sizer.Fit(scroll_panel)

        button_sizer.Add(self.help_button, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        button_sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        button_sizer.Add(self.cancel_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        button_sizer.Add(self.submit_button, 0, wx.EXPAND | wx.ALL, 5)
        bottom_panel.SetSizer(button_sizer)

        frame_sizer.Add(scroll_panel, proportion=1, flag=wx.LEFT | wx.EXPAND, border=-10)
        frame_sizer.Add(break_line, 0, wx.EXPAND, 5)
        frame_sizer.Add(bottom_panel, 0, wx.ALL | wx.EXPAND, 3)

        panel.SetSizer(frame_sizer)
        frame_sizer.Fit(self)
        self.SetSize((-1, 400))

        self.Show()
