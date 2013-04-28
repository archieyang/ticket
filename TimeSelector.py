# coding=utf-8
import wx


class TimeSelector(wx.BoxSizer):

    """docstring for TimeSelector"""
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        comboStyle = wx.CB_DROPDOWN | wx.CB_READONLY
        self.hourCombo = wx.ComboBox(panel, size=(95, -1),
                                     choices=[str(x) for x in range(0, 24)],
                                     style=comboStyle)
        self.minCombo = wx.ComboBox(panel, size=(95, -1),
                                    choices=[str(x) for x in range(0, 60)],
                                    style=comboStyle)
        self.AddMany([self.hourCombo, self.minCombo])

    def getValue(self):
        h = self.hourCombo.GetValue()
        m = self.minCombo.GetValue()
        if h is None or m is None:
            return None

        if len(h) < 2:
            h = "0" + h
        if len(m) < 2:
            m = "0" + m
        return h + ":" + m
