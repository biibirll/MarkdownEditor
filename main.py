import sys
import wx
import wx.html2
import markdown2


class MarkdownEditor(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        splitter = wx.SplitterWindow(self)
        left_pane = wx.TextCtrl(splitter, style=wx.TE_MULTILINE)
        right_pane = wx.html2.WebView.New(splitter)
        splitter.SplitVertically(left_pane, right_pane, 250)
        splitter.SetSashGravity(0.5)

        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r') as f:
                text = f.read()
                left_pane.SetValue(text)
                html = markdown2.markdown(text)
                right_pane.SetPage(html, "")

        self.left_pane = left_pane
        self.right_pane = right_pane

        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        new_menu_item = file_menu.Append(
            wx.ID_NEW, "New\tCtrl+N", "Create a new Markdown file"
        )
        open_menu_item = file_menu.Append(
            wx.ID_OPEN, "Open\tCtrl+O", "Open a Markdown file"
        )
        save_menu_item = file_menu.Append(
            wx.ID_SAVE, "Save\tCtrl+S", "Save the Markdown file"
        )
        menubar.Append(file_menu, "File")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnOpen, open_menu_item)
        self.Bind(wx.EVT_MENU, self.OnSave, save_menu_item)
        self.Bind(wx.EVT_MENU, self.OnNew, new_menu_item)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_TEXT, self.OnTextChange, left_pane)

    def OnOpen(self, event):
        file_dialog = wx.FileDialog(
            self,
            "Open Markdown file",
            wildcard="Markdown files (*.md)|*.md",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        )

        def ShowAndProcess():
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path = file_dialog.GetPath()
            with open(path, "r") as f:
                text = f.read()

            self.left_pane.SetValue(text)
            self.OnTextChange(None)

        wx.CallAfter(ShowAndProcess)

    def OnSave(self, event):
        file_dialog = wx.FileDialog(
            self,
            "Save Markdown file",
            wildcard="Markdown files (*.md)|*.md",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )

        def ShowAndProcess():
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            path = file_dialog.GetPath()
            with open(path, "w") as f:
                text = self.left_pane.GetValue()
                f.write(text)

        wx.CallAfter(ShowAndProcess)

    def OnNew(self, event):
        self.left_pane.SetValue("")
        self.OnTextChange(None)

    def OnKeyDown(self, event):
        key_code = event.GetKeyCode()

        if event.ControlDown():
            if key_code == 79:
                self.OnOpen(None)
            elif key_code == 83:
                self.OnSave(None)
            elif key_code == 78:
                self.OnNew(None)
        event.Skip()

    def OnTextChange(self, event):
        text = self.left_pane.GetValue()
        html = markdown2.markdown(text)
        self.right_pane.SetPage(html, "")


if __name__ == "__main__":
    app = wx.App()
    frame = MarkdownEditor(None, "Markdown Editor")
    app.MainLoop()
