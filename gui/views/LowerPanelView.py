import wx
from gui.controller.ConsoleOutputCtrl import consoleCtrl
from gui.controller.TimeSeriesCtrl import TimeSeriesCtrl
from gui.controller.SimulationsTabCtrl import SimulationsTabCtrl


class ViewLowerPanel:
    def __init__(self, notebook):
        self.notebook = notebook
        self.current_tab = 0

        console = consoleCtrl(notebook)
        self.timeseries = TimeSeriesCtrl(notebook)
        simulations = SimulationsTabCtrl(notebook)
        notebook.AddPage(console, "Console")
        notebook.AddPage(self.timeseries, "Time Series")
        notebook.AddPage(simulations, "Simulations")
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_changed)

    def on_tab_changed(self, event):
        if event.GetSelection() == self.current_tab:
            return
        self.current_tab = event.GetSelection()
        event.GetEventObject().SetSelection(self.current_tab)
        if self.current_tab == 1:
            self.timeseries.load_connection_combo()
        return
