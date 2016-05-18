from gui.views.PropertiesPageView import PropertiesPageView
import wx


class PropertiesPageCtrl(PropertiesPageView):
    def __init__(self, parent):

        PropertiesPageView.__init__(self, parent)
        self.enable_drag_grid_size()
        self.parent = parent
        self.enable_editing(False)

        # Key is section, value is section position in the grid
        self.__section_row_number = {-1: -1}
        self.Bind(wx.EVT_SIZE, self.frame_resizing)

    def add_section(self, name):
        max_position = self.get_max_section_position() # rename max_position to section
        # Create a new row that will become the section
        self.grid.InsertRows(pos=self.__section_row_number[max_position] + 1)

        # Set the cell to expand and fill the size of the grid
        self.grid.SetCellSize(row=self.__section_row_number[max_position] + 1, col=0, num_rows=1, num_cols=self.grid.GetNumberCols())

        # Set the section title
        self.grid.SetCellValue(self.__section_row_number[max_position] + 1, 0, str(name))

        self.grid.SetCellBackgroundColour(self.__section_row_number[max_position] + 1, 0, wx.Colour(186, 195, 211))

        # Add the new created section to the dictionary for storage
        self.__section_row_number[max_position + 1] = self.grid.GetNumberRows() - 1

    def add_data_to_section(self, section, key, value):
        """
        :param section:
        :param key: Left column
        :param value: Right column
        :return: True if insertion was successful, else False
        """
        if section in self.__section_row_number:

            self.grid.InsertRows(pos=self.__section_row_number[section] + 1)
            self.grid.SetCellValue(self.__section_row_number[section] + 1, 0, str(key))
            self.grid.SetCellValue(self.__section_row_number[section] + 1, 1, str(value))
            self._update_section()
            self.grid.AutoSize()
            self._min_grid_width_size = self.get_grid_width()
            return True

        # Section does not exist
        return False

    def add_data(self, data):
        """
        :param data: Must be a dictionary, where the values are a list of dictionaries
        :return:
        """
        sorted_sections = sorted(data.keys())
        section = 0
        for each_section in sorted_sections:
            if isinstance(data[each_section], list):
                self.add_section(each_section)
                for sub_data in data[each_section]:
                    for k, v in sub_data.iteritems():
                        self.add_data_to_section(section, k, v)
                section += 1

        self.enable_scroll_bar_on_startup()

    def enable_drag_grid_size(self, enable=False):
        self.grid.EnableDragGridSize(enable)

    def enable_editing(self, enable=True):
        self.grid.EnableEditing(enable)

    def enable_grid_lines(self, enable=True):
        self.grid.EnableGridLines(enable)

    def enable_scroll_bar_on_startup(self):
        """
        Enables the scroll bars after loading data.
        :return:
        """
        x, y = self.GetSize()
        self.SetSize((x + 1, y + 1))

    def get_max_section_position(self):
        max_position = -1
        for key, value in self.__section_row_number.iteritems():
            if key > max_position:
                max_position = key
        return max_position

    def _update_section(self):
        """
        Update the values in the section. The value is the row on the grid the section is at
        :return:
        """
        for i in range(len(self.__section_row_number) - 1):
            self.__section_row_number[i] += 1

    ###############################
    # EVENTS
    ###############################

    def frame_resizing(self, event):
        #  Handles resizing the grid so the content is always show
        if self.GetSize()[0] < self._min_grid_width_size:
            self.restore_min_grid_width()
        else:
            self.resize_grid_to_fill_white_space()
        event.Skip()
