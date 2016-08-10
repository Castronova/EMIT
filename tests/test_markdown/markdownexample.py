import wx
import wx.html
from wx.html import HtmlWindow
import markdown


class MarkdownExample(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        document = open('document.md', 'r')

        html = markdown.markdown(document.read())  # Read the whole file

        self.html_window = HtmlWindow(self)
        self.html_window.SetPage(html)

        self.Show()



if __name__ == '__main__':

    app = wx.App()
    MarkdownExample(None)
    app.MainLoop()
