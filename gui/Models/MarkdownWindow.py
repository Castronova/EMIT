from wx.html import HtmlWindow
import wx
import markdown


class MarkdownWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)
        self.html_window = HtmlWindow(self)
        self.Show()

    def read_markdown_file(self, file_path):
        document = open(file_path, 'r')
        html = markdown.markdown(document.read())
        self.html_window.SetPage(html)

    def read_markdown_text(self, text):
        html = markdown.markdown(text)
        self.html_window.SetPage(html)
