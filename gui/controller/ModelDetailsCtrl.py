from gui.views.ModelDetailsView import ModelDetailsView
import wx


class ModelDetailsCtrl(ModelDetailsView):
    def __init__(self, parent):
        ModelDetailsView.__init__(self)
        self.enable_drag_grid_size()
        self.parent = parent
        self.enable_editing(False)

        # Key is section, value is section position in the grid
        self.__section_row_number = {-1: -1}
        self.grid.SetScrollLineY(15)

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

    def enable_drag_grid_size(self, enable=False):
        self.grid.EnableDragGridSize(enable)

    def enable_editing(self, enable=True):
        self.grid.EnableEditing(enable)

    def enable_grid_lines(self, enable=True):
        self.grid.EnableGridLines(enable)

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
