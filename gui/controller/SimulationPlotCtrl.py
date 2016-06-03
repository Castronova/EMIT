import wx
from gui.views.SimulationsPlotView import SimulationsPlotView


class SimulationsPlotCtrl(SimulationsPlotView):
    def __init__(self, parent, columns=None):
        SimulationsPlotView.__init__(self, parent)

        if columns:
            self.table.set_columns(columns)

        self.plot_button.Bind(wx.EVT_BUTTON, self.on_plot)

        self.data = {}  # Dictionary to hold the data respective to the row ID

    def get_selected_id(self):
        """
        :return: the ID type(Int) of the selected row or -1 if no row is selected
        """
        row = self.table.get_selected_row()
        if row:
            return int(row[0])
        return -1

    ##########################
    # EVENTS
    ##########################

    def on_plot(self, event):
        """
        Grabs the data related to the selected row. self.data must be set otherwise it will not plot
        :param event:
        :return: True if plot was successful, False if plot failed
        """
        ID = self.get_selected_id()

        if ID == -1:
            return False  # No selected row

        if not len(self.data) or ID not in self.data:
            return False  # self.data has not been set or set incorrectly

        date_time_objects, value = self.data[ID]

        data = []
        for i in range(len(date_time_objects)):
            data.append((date_time_objects[i], value[i]))

        name = self.table.get_selected_row()[1]
        units = self.table.get_selected_row()[2]
        self.temporal_plot.clearPlot()
        self.temporal_plot.plotData(data, name, None, units)
        return True
