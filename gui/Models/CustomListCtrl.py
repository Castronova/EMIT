import wx


class CustomListCtrl(wx.ListCtrl):
    def __init__(self, panel):
        wx.ListCtrl.__init__(self, panel, style=wx.LC_REPORT)

        # Message to show in the ListCtrl when it is empty
        self.empty_list_message = wx.StaticText(parent=self, label="This list is empty",
                                                style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE | wx.FULL_REPAINT_ON_RESIZE)
        self.empty_list_message.Hide()
        self.empty_list_message.SetForegroundColour(wx.LIGHT_GREY)
        self.empty_list_message.SetBackgroundColour(self.GetBackgroundColour())
        self.empty_list_message.SetFont(wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_list_column_clicked)
        self.Bind(wx.EVT_SIZE, self._handle_table_resizing)

    def on_list_column_clicked(self, event):
        self.__sort_table_by_column(event.GetColumn())

    def alternate_row_color(self, color="#DCEBEE"):
        for i in range(self.GetItemCount()):
            if i % 2 == 0:
                self.SetItemBackgroundColour(i, color)

    def auto_size_table(self):
        for i in range(self.GetColumnCount()):
            self.SetColumnWidth(col=i, width=wx.LIST_AUTOSIZE)
        self.expand_table_to_fill_panel()

    def clear_table(self):
        """
        Clears everything in the table including the header names
        :return:
        """
        self.ClearAll()

    def clear_content(self):
        """
        Clears everything in the table except the header names
        :return:
        """
        self.DeleteAllItems()

    def expand_table_to_fill_panel(self):
        """
        Sets the width of the table to fill up any white space
        :return:
        """
        if not self.GetColumnCount():
            return
        last_column_index = self.GetColumnCount() - 1
        size = self.GetTopLevelParent().GetSize()[0]
        self.SetColumnWidth(last_column_index, size)

    def get_all_selected_rows(self):
        """
        Gets all the selected rows
        :return: 2D list, list(rows)
        """
        index = self.GetFirstSelected()
        if index == -1:
            return []  # No selected row

        data = [self.get_row_at_index(index)]
        for i in range(self.GetSelectedItemCount() - 1):
            index = self.GetNextSelected(index)
            data.append(self.get_row_at_index(index))

        return data

    def get_row_at_index(self, index):
        """
        Given a row number, return all the data related to the row
        :param index: int
        :return: list
        """
        if index > self.GetItemCount():
            return []  # There are not that many rows in the table

        data = []
        for i in range(self.GetColumnCount()):
            data.append(self.GetItem(index, i).GetText())
        return data

    def get_all_data_in_table(self):
        data = []
        for i in range(self.GetItemCount()):
            data.append(self.get_row_at_index(i))
        return data

    def __sort_table_by_column(self, column_number):
        if column_number < 0:
            return

        data = self.get_all_data_in_table()

        column_data = []
        for i in data:
            column_data.append(i[column_number])

        column_data.sort()

        new_data = []
        for i in range(len(column_data)):
            for j in range(len(data)):
                if column_data[i] in data[j]:
                    new_data.append(data[j])
                    break

        # write the data back
        self.clear_content()
        self.set_table_content(new_data)

    def get_selected_row(self):
        """
        Gets the first selected row
        :return: data: type(list). Return None if no row is selected
        """
        row_number = self.GetFirstSelected()
        if row_number == -1:
            return None

        data = []
        for i in range(self.GetColumnCount()):
            data.append(self.GetItem(row_number, i).GetText())
        return data

    def _handle_table_resizing(self, event):
        event.Skip()
        self.expand_table_to_fill_panel()
        size = self.GetClientSize()
        self.empty_list_message.SetDimensions(0, size.GetHeight() / 3, size.GetWidth(), size.GetHeight())

    def set_columns(self, columns):
        """
        Sets the name of the columns
        :param columns: a list of strings
        :return:
        """
        self.clear_table()
        for i in range(len(columns)):
            self.InsertColumn(i, columns[i], width=wx.LIST_AUTOSIZE_USEHEADER)

    def set_empty_message_text(self, text):
        self.empty_list_message.SetLabel(text)

    def set_table_content(self, data):
        """
        data must be a 2D list [[row1 column1, row1 column2, ...], [row2, column1, row2 column2, ...]]
        :param data: 2D list
        :return:
        """

        number_of_columns = self.GetColumnCount()
        if number_of_columns == 0:
            print "No column headers have been created"
            return

        # loop through all of the site metadata
        for i in range(len(data)):
            index = self.InsertStringItem(999999, "")
            if number_of_columns < len(data[i]):
                raise Exception("The length of the row must match the number of columns")

            for j in range(len(data[i])):
                self.SetStringItem(index, j, str(data[i][j]))

        self.auto_size_table()
        self.alternate_row_color()
