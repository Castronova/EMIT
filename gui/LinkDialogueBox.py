__author__ = 'Mario'

import wx, wx.html
import sys

#aboutText = """<p>Sorry, there is no information about this program. It is
#running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
#See <a href="http://wiki.wxpython.org">wxPython Wiki</a></p>"""

aboutLink = """<p> This link is between % (M1) and % (M2)."""

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

class LinkBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About Link",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400,200))
        #vers = {}
        #vers["python"] = sys.version.split()[0]
        #vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutLink)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

'''
class Example(wx.Dialog):

    def __init__(self, *args, **kwargs):


        self.InitMenu()

    def InitMenu(self):

        menubar = wx.MenuBar()
        help = wx.Menu()
        help.Append(100, '&About')
        self.Bind(wx.EVT_MENU, self.OnAboutBox, id=100)
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)

        self.SetSize((300, 200))
        self.SetTitle('About dialog box')
        self.Centre()
        self.Show(True)

    def OnAboutBox(self, e):

        description = """File Hunter is an advanced file manager for
the Unix operating system. Features include powerful built-in editor,
advanced search capabilities, powerful batch renaming, file comparison,
extensive archive handling and more.
"""

        licence = """File Hunter is free software; you can redistribute
it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

File Hunter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details. You should have
received a copy of the GNU General Public License along with File Hunter;
if not, write to the Free Software Foundation, Inc., 59 Temple Place,
Suite 330, Boston, MA  02111-1307  USA"""


        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG))
        info.SetName('File Hunter')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2007 - 2011 Jan Bodnar')
        info.SetWebSite('http://www.zetcode.com')
        info.SetLicence(licence)
        info.AddDeveloper('Jan Bodnar')
        info.AddDocWriter('Jan Bodnar')
        info.AddArtist('The Tango crew')
        info.AddTranslator('Jan Bodnar')
'''
        #wx.LinkBox(info)
