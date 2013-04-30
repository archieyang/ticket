# coding=utf-8
import wx


class TimeSelector(wx.BoxSizer):

    """docstring for TimeSelector"""
    def __init__(self, panel):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        comboStyle = wx.CB_DROPDOWN | wx.CB_READONLY
        hCandidate = [str(x) for x in range(0, 24)]
        for i in range(0, 9):
            hCandidate[i] = "0" + hCandidate[i]
        self.hourCombo = wx.ComboBox(panel, size=(95, -1),
                                     choices=hCandidate,
                                     style=comboStyle)
        mCandidate = [str(x) for x in range(0, 60)]
        for i in range(0, 9):
            mCandidate[i] = "0" + mCandidate[i]
        self.minCombo = wx.ComboBox(panel, size=(95, -1),
                                    choices=mCandidate,
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
    def setValue(self, formatted_time):
        self.hourCombo.SetValue(formatted_time[0:2])
        self.minCombo.SetValue(formatted_time[3:5])
