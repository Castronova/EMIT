from wx.html import HtmlWindow
import wx
import markdown


class MarkdownWindow(wx.Frame):
    def __init__(self, parent, text):
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)

        self.markdown = markdown.Markdown()

        # page = """Line 1 <br />
        #  Line 2 <br /> _italics_
        #  <br />
        #  **BOLD**
        # `hello`
        #  """
        html = self.markdown.convert(text)

        self.html_window = HtmlWindow(self)
        self.html_window.SetPage(html)


        self.Show()
