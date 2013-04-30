# coding=utf-8
import MainPanel
import wx
app = wx.App(False)
frame = wx.Frame(None, title='B12306', size=(700, 500))
panel = MainPanel.MPanel(frame)
frame.Show()
app.MainLoop()
