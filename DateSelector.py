# coding=utf-8
import wx


class DateSelector(wx.BoxSizer):

    """docstring for DateSelecor"""
    def __init__(self, panel):
        wx.BoxSizer.__init__(self)
        comboStyle = wx.CB_DROPDOWN | wx.CB_READONLY

        self.yearCombo = wx.ComboBox(panel, size=(40, -1),
                                     choices=[str(x) for x in range(2013, 2031)],
                                     style=comboStyle)
        self.monthCombo = wx.ComboBox(panel, size=(40, -1),
                                      choices=[str(x) for x in range(1, 13)],
                                      style=comboStyle)
        self.dayList = [str(x) for x in range(1, 32)]
        self.dayCombo = wx.ComboBox(panel, size=(40, -1),
                                    choices=self.dayList,
                                    style=comboStyle)

        self.AddMany([self.yearCombo, self.monthCombo, self.dayCombo])

    def getValue(self):
        year = self.yearCombo.GetValue()
        mon = self.monthCombo.GetValue()
        day = self.dayCombo.GetValue()

        if year is None or mon is None or day is None:
            return None

        if len(mon) < 2:
            mon = "0" + mon
        if len(day) < 2:
            day = "0" + day

        return year + "-" + mon + "-" + day
