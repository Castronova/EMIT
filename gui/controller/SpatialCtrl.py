import wx
from osgeo import ogr
import stdlib
from coordinator import engineAccessors
from emitLogging import elog
from gui.views.SpatialView import SpatialView
from sprint import *


class SpatialCtrl(SpatialView):

    def __init__(self, panel):
        SpatialView.__init__(self, panel)

        self.raw_input_data = None
        self.raw_output_data = None

        self.__input_data = None
        self.__output_data = None
        self.input_legend_label = ""
        self.output_legend_label = ""

        # Set the combo box to ---
        self.input_combobox.SetSelection(0)
        self.output_combobox.SetSelection(0)
        self.input_combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.output_combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.plot.set_axis_label("my X axis", "My y axis")
        panel.Bind(wx.EVT_SIZE, self.frame_resizing)

    def frame_resizing(self, event):
        self.resize_grid_to_fill_white__space(self.input_grid)
        self.resize_grid_to_fill_white__space(self.output_grid)
        event.Skip()

    def resize_grid_to_fill_white__space(self, grid):
        col_size = grid.GetColSize(0)
        C, R = grid.GetSize()
        if C - col_size > 0:
            grid.SetColSize(1, C - col_size)

    def add_input_combo_choices(self, items):
        self.input_combobox.AppendItems(items)

    def add_output_combo_choices(self, items):
        self.output_combobox.AppendItems(items)

    def clear_grid(self, type):
        """
        clears the metadata from the input/output exchange item grids
        :param type: type if echange item 'input' or 'output'
        :return: None
        """

        if type == 'input':
            for row in range(1, self.input_grid.GetNumberRows()):
                self.clear_cell(self.input_grid, row, 1)
        elif type == 'output':
            for row in range(1, self.output_grid.GetNumberRows()):
                self.clear_cell(self.output_grid, row, 1)

    def clear_cell(self, grid, row, col):
        grid.SetCellValue(row, col, '')

    def edit_grid(self, grid, x_loc, y_loc, value):
        if grid == "input":
            grid = self.input_grid

        if grid == "output":
            grid = self.output_grid

        grid.SetCellValue(x_loc, y_loc, str(value))

    def get_color_by_plot_name(self, name):
        if name in self.__input_data:
            return "#019477"
        if name in self.__output_data:
            return "#0DACFF"

    def get_exchange_items_names(self, model_id, model_type="INPUT"):
        # model_type must match INPUT or OUTPUT
        items = engineAccessors.getExchangeItems(modelid=model_id, exchange_item_type=model_type.upper(), returnGeoms=False)
        if items is not None:
            return [item['name'] for item in items]
        return [""]

    def get_input_combo_choices(self):
        items = []
        for i in range(self.input_combobox.GetCount()):
            items.append(self.input_combobox.GetString(i))
        return items

    def get_output_combo_choies(self):
        items = []
        for i in range(self.output_combobox.GetCount()):
            items.append(self.output_combobox.GetString(i))
        return items

    def get_input_exchange_item_by_id(self, id):
        return engineAccessors.getExchangeItems(id, 'INPUT')

    def get_output_exchange_item_by_id(self, id):
        return engineAccessors.getExchangeItems(id, 'OUTPUT')

    def get_geometries(self, exchange_item):  # This method should work for both input and output
        if isinstance(exchange_item, list):
            igeoms = {}
            for item in exchange_item:
                name = item['name']
                geoms = [ogr.CreateGeometryFromWkb(g) for g in item['geometry']['wkb']]
                igeoms[name] = geoms
            return igeoms
        else:
            elog.debug("Exchange item must be a list of dictionaries")
            elog.debug("Exchange item may be None")
            return {}

    def get_geoms_by_name(self, name):
        if name in self.__input_data:
            return self.__input_data[name]

        if name in self.__output_data:
            return self.__output_data[name]
        return None

    def get_item_in_raw_data(self, raw_data, item):
        if raw_data:
            for data in raw_data:
                if data.has_key("name"):
                    if data["name"] == item:
                        return data
        return None  # None if item not found in raw_data

    def get_selected_input_exchange_item(self):
        if self.input_combobox.GetValue() == "---":
            return {}

        return {self.input_combobox.GetValue(): self.__input_data[self.input_combobox.GetValue()][0]}

    def get_selected_output_exchange_item(self):
        if self.output_combobox.GetValue() == "---":
            return {}

        return {self.output_combobox.GetValue(): self.__output_data[self.output_combobox.GetValue()][0]}

    def on_combo(self, event):
        self.plot.clear_plot()
        if self.input_combobox.GetValue() == "---":
            self.input_legend_label = ""
            self.clear_grid('input')
        else:
            self.input_legend_label = self.input_combobox.GetValue()
            self.update_plot(self.input_combobox.GetValue())
            self.update_ei_table(stdlib.ExchangeItemType.INPUT)

        if self.output_combobox.GetValue() == "---":
            self.output_legend_label = ""
            self.clear_grid('output')
        else:
            self.output_legend_label = self.output_combobox.GetValue()
            self.update_plot(self.output_combobox.GetValue())
            self.update_ei_table(stdlib.ExchangeItemType.OUTPUT)

    def set_data(self, target={}, source={}):  # target is input, source is output
        self.__input_data = target
        self.__output_data = source

    def set_legend(self, location=0):
        labels = []
        if self.input_legend_label:
            labels.append(self.input_legend_label)
        if self.output_legend_label:
            labels.append(self.output_legend_label)

        self.plot.axes.legend(labels, loc=location)

    def update_plot(self, data_in, plot_title=""):
        # Data_in is the variable name
        data = self.get_geoms_by_name(data_in)
        if data is None:
            return

        # We can use either a set color or use the getNextColor() from SpatialTemporalPlotter.pyy
        # color = self.plot.getNextColor()
        # color = "#019477"
        color = self.get_color_by_plot_name(data_in)

        self.plot.plot_geometry(data, color, plot_title)
        self.set_legend()
        self.plot.redraw()

    def update_ei_table(self, type=stdlib.ExchangeItemType.INPUT):

        # get the selected item (either input or output)
        if type == stdlib.ExchangeItemType.INPUT:
            item = self.get_selected_input_exchange_item()
            data = self.raw_input_data
        else:
            item = self.get_selected_output_exchange_item()
            data = self.raw_output_data

        # get the metadata for this exchange item
        raw_data = self.get_item_in_raw_data(data, item.keys()[0])

        # populate the exchange item table
        if raw_data:
            self.edit_grid(type.lower(), 1, 1, item.keys()[0])
            self.edit_grid(type.lower(), 2, 1, item.values()[0].GetGeometryName())
            self.edit_grid(type.lower(), 3, 1, raw_data["geometry"]["count"])
            self.edit_grid(type.lower(), 4, 1, item.values()[0].GetCoordinateDimension())
            self.edit_grid(type.lower(), 5, 1, raw_data["geometry"]["extent"])
        else:
            msg = 'Failed to populate exchange item metadata'
            elog.error(msg)
            sPrint(msg, MessageType.ERROR)
