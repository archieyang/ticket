# coding=utf-8
import wx
import time
import datetime


class DateSelector(wx.BoxSizer):

    """docstring for DateSelecor"""
    LONG_MONTH = ['01', '03', '05', '07', '08', '10', '12']

    def __init__(self, panel):
        wx.BoxSizer.__init__(self)
        comboStyle = wx.CB_DROPDOWN | wx.CB_READONLY

        self.yearCombo = wx.ComboBox(panel, size=(100, -1),
                                     choices=[str(x) for x in range(2013, 2031)],
                                     style=comboStyle)
        monthCandidate = [str(x) for x in range(1, 13)]
        self.formation(monthCandidate)
        self.monthCombo = wx.ComboBox(panel, size=(40, -1),
                                      choices= monthCandidate,
                                      style=comboStyle)
        self.dayList = [str(x) for x in range(1, 32)]
        self.formation(self.dayList)
        self.dayCombo = wx.ComboBox(panel, size=(40, -1),
                                    choices=self.dayList,
                                    style=comboStyle)

        self.AddMany([self.yearCombo, self.monthCombo, self.dayCombo])
        ISOTIMEFORMAT = '%Y%m%d'
        today = time.strftime(ISOTIMEFORMAT, time.localtime())

        panel.Bind(wx.EVT_COMBOBOX, self.monthEvt, self.monthCombo)
        panel.Bind(wx.EVT_COMBOBOX, self.yearEvt, self.yearCombo)

        self.yearCombo.SetValue(today[0:4])
        self.monthCombo.SetValue(today[4:6])
        self.monthEvt(wx.EVT_COMBOBOX)
        self.dayCombo.SetValue(today[6:8])

    def monthEvt(self, event):
        month = self.monthCombo.GetValue()
        self.dayCombo.Clear()
        if month == "02":
            if (not self.isLeapYear()):
                self.dayCombo.AppendItems(self.formation([str(x) for x in range(1, 29)]))
            else:
                self.dayCombo.AppendItems(self.formation([str(x) for x in range(1, 30)]))
        elif month in DateSelector.LONG_MONTH:
            self.dayCombo.AppendItems(self.formation([str(x) for x in range(1, 32)]))
        else:
            self.dayCombo.AppendItems(self.formation([str(x) for x in range(1, 31)]))

    def yearEvt(self, event):
        if self.monthCombo.GetValue() != "02":
            return
        self.dayCombo.Clear()
        if self.isLeapYear():
            self.dayCombo.AppendItems(self.formation([str(x) for x in range(1, 30)]))
        else:
            self.dayCombo.AppendItems(self.formation([str(x) for x in range(1, 29)]))

    def formation(self, sList):
        for i in range(0, 9):
            sList[i] = "0" + sList[i]
        return sList

    def isLeapYear(self):
        yearNum = (int)(self.yearCombo.GetValue())
        if (yearNum % 4 == 0 and yearNum % 100 != 0) or yearNum % 400 == 0:
            return True
        return False

    def getValue(self):
        year = self.yearCombo.GetValue()
        mon = self.monthCombo.GetValue()
        day = self.dayCombo.GetValue()

        if year is None or mon is None or day is None:
            return None

        return datetime.date(int(year), int(mon), int(day))

    def setValue(self, iso_date):
        self.yearCombo.SetValue(iso_date[0:4])
        self.yearEvt(None)
        self.monthCombo.SetValue(iso_date[5:7])
        self.monthEvt(None)
        self.dayCombo.SetValue(iso_date[8:10])
