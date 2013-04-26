# coding=utf-8
import wx


class MultiCheckBox(wx.BoxSizer):

    """docstring for MultiCheckBox"""
    def __init__(self, panel, argList):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.panel = panel
        for s in argList:
            cb = wx.CheckBox(panel, label=s)
            self.Add(cb)
