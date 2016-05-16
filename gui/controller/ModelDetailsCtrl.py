from gui.views.ModelDetailsView import ModelDetailsView
import wx

class ModelDetailsCtrl(ModelDetailsView):
    def __init__(self, parent):
        ModelDetailsView.__init__(self)
        self.enable_drag_grid_size()
        self.parent = parent
        self.enable_editing(False)

        self.__section_row_number = [-1]

        self.add_section("General")
        self.add_section("Input")
        self.add_section("Output")
        self.add_data_to_section(0, "first data point", "something else")

    def add_section(self, name):
        # Create a new row that will become the section
        self.grid.InsertRows(pos=self.__section_row_number[-1] + 1)

        # Set the cell to expand and fill the size of the grid
        self.grid.SetCellSize(row=self.__section_row_number[-1] + 1, col=0, num_rows=1, num_cols=self.grid.GetNumberCols())

        # Set the section title
        self.grid.SetCellValue(self.__section_row_number[-1] + 1, 0, str(name))

        self.grid.SetCellBackgroundColour(self.__section_row_number[-1] + 1, 0, wx.Colour(250, 250, 250))
        self.__section_row_number.append(self.__section_row_number[-1] + 1)

    def add_data_to_section(self, section, key, value):
        """
        :param section:
        :param key: Left column
        :param value: Right column
        :return: True if insertion was successful, else False
        """
        if section in self.__section_row_number:

            self.grid.InsertRows(pos=section + 1)
            self.grid.SetCellValue(section + 1, 0, str(key))
            self.grid.SetCellValue(section + 1, 1, str(value))
            self.grid.AutoSize()
            self.resize_window_to_fit()
            return True

        # Section does not exist
        return False

    def enable_drag_grid_size(self, enable=False):
        self.grid.EnableDragGridSize(enable)

    def enable_editing(self, enable=True):
        self.grid.EnableEditing(enable)

    def enable_grid_lines(self, enable=True):
        self.grid.EnableGridLines(enable)
