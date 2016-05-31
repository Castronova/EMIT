import wx


class TimeSeriesView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Components
        self.connection_options = ["---"]
        self.connection_combo = wx.Choice(self, size=(200, -1), choices=self.connection_options)
        self.add_connection_button = wx.Button(self, label="Add Connection")
        self.refresh_button = wx.Button(self, label="Refresh")
        self.table = wx.ListCtrl(self, style=wx.LC_REPORT)

        # Message to show in the ListCtrl when it is empty
        self.empty_list_message = wx.StaticText(parent=self.table, label="This list is empty",
                                                style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE | wx.FULL_REPAINT_ON_RESIZE)
        self.empty_list_message.Hide()
        self.empty_list_message.SetForegroundColour(wx.LIGHT_GREY)
        self.empty_list_message.SetBackgroundColour(self.table.GetBackgroundColour())
        self.empty_list_message.SetFont(wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))

        # Pop up menu
        self.popup_menu = wx.Menu()
        self.view_menu = self.popup_menu.Append(1, "View")

        # Create sizers
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add components to sizer
        button_sizer.Add(self.connection_combo, 0, wx.ALL, 5)
        button_sizer.Add(self.add_connection_button, 0, wx.ALL, 5)
        button_sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        button_sizer.Add(self.refresh_button, 0, wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.table, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(main_sizer)

        # Events
        self.table.Bind(wx.EVT_SIZE, self._handle_table_resizing)

    def alternate_row_color(self, color="#DCEBEE"):
        for i in range(self.table.GetItemCount()):
            if i % 2 == 0:
                self.table.SetItemBackgroundColour(i, color)

    def append_to_connection_combo(self, item):
        if item in self.connection_options:  # Do not add duplicate items
            return
        self.connection_options.append(item)
        self.connection_options.sort()
        self.connection_combo.SetItems(self.connection_options)

    def auto_size_table(self):
        for i in range(self.table.GetColumnCount()):
            self.table.SetColumnWidth(col=i, width=wx.LIST_AUTOSIZE)
        self.expand_table_to_fill_panel()

    def clear_table(self):
        """
        Clears everything in the table including the header names
        :return:
        """
        self.table.ClearAll()

    def clear_content(self):
        """
        Clears everything in the table except the header names
        :return:
        """
        self.table.DeleteAllItems()

    def expand_table_to_fill_panel(self):
        """
        Sets the width of the table to fill up any white space
        :return:
        """
        last_column_index = self.table.GetColumnCount() - 1
        size = self.GetTopLevelParent().GetSize()[1]
        self.table.SetColumnWidth(last_column_index, size)

    def get_selected_row(self):
        """
        Gets the first selected row
        :return: data: type(list)
        """
        row_number = self.table.GetFirstSelected()
        data = []
        for i in range(self.table.GetColumnCount()):
            data.append(self.table.GetItem(row_number, i).GetText())
        return data

    def _handle_table_resizing(self, event):
        event.Skip()
        size = self.table.GetClientSize()
        self.empty_list_message.SetDimensions(0, size.GetHeight() / 3, size.GetWidth(), size.GetHeight())

    def set_columns(self, columns):
        """
        Sets the name of the columns
        :param columns: a list of strings
        :return:
        """
        self.clear_table()
        for i in range(len(columns)):
            self.table.InsertColumn(i, columns[i], width=wx.LIST_AUTOSIZE_USEHEADER)

    def set_table_content(self, data):
        """
        :param data: 2D list
        :return:
        """
        if self.table.GetColumnCount() == 0:
            print "No column headers have been created"
            return

        for i in range(len(data)):
            index = self.table.InsertStringItem(999999, "")
            for j in range(len(data[i])):
                self.table.SetStringItem(index, j, data[i][j])

        self.auto_size_table()
        self.alternate_row_color()
