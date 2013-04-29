# coding=utf-8
import wx
import checker
from checker import ticket_type, train_class
from MultiCheckBox import MultiCheckBox
from TimeSelector import TimeSelector
from DateSelector import DateSelector


class MPanel(wx.Panel):

    """docstring for ClassName"""
    def __init__(self, parent):
        self.checking = False
        date = "Date"
        fromCity = 'From'
        toCity = 'To'
        time = 'Time'
        seat = 'Seat'
        email = 'Email'
        start = 'Start'
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        cityBox = wx.BoxSizer(wx.HORIZONTAL)
        wx.Panel.__init__(self, parent)
        self.fromCityLabel = wx.StaticText(self, label=fromCity)
        self.fromCityInput = wx.TextCtrl(self, size=(140, -1))
        self.toCityLabel = wx.StaticText(self, label=toCity)
        self.toCityInput = wx.TextCtrl(self, size=(140, -1))
        cityBox.Add(self.fromCityLabel)
        cityBox.Add(self.fromCityInput)
        cityBox.Add(self.toCityLabel)
        cityBox.Add(self.toCityInput)

        dateBox = wx.BoxSizer(wx.HORIZONTAL)
        self.dateLabel = wx.StaticText(self, label=date)

        self.startDateCombo = DateSelector(self)
        dateBox.AddMany([self.dateLabel, self.startDateCombo])

        timeBox = wx.BoxSizer(wx.HORIZONTAL)
        self.timeLabel = wx.StaticText(self, label=time)
        self.timeInputFrom = TimeSelector(self)
        self.timeInputTo = TimeSelector(self)
        timeBox.Add(self.timeLabel)
        timeBox.Add(self.timeInputFrom)
        timeBox.Add(self.timeInputTo)

        self.classCheckBoxGroup = MultiCheckBox(self, train_class)
        self.typeCheckBoxGroup = MultiCheckBox(self, ticket_type)

        mailBox = wx.BoxSizer(wx.VERTICAL)
        self.mailLabel = wx.StaticText(self, label=email)
        self.mailInput = wx.TextCtrl(self, size=(140, -1))
        mailBox.Add(self.mailLabel)
        mailBox.Add(self.mailInput)

        self.startButton = wx.Button(self, label=start)
        self.Bind(wx.EVT_BUTTON, self.OnStartClick, self.startButton)

        self.log = wx.TextCtrl(self, -1, "",
                               style=wx.TE_RICH | wx.TE_MULTILINE)

        mainSizer.Add(cityBox, 0, wx.ALL, 5)
        mainSizer.Add(dateBox, 0, wx.ALL, 5)
        mainSizer.Add(timeBox, 0, wx.ALL, 5)
        mainSizer.Add(self.classCheckBoxGroup, 0, wx.ALL, 5)
        mainSizer.Add(self.typeCheckBoxGroup, 0, wx.ALL, 5)
        mainSizer.Add(mailBox, 0, wx.ALL, 5)
        mainSizer.Add(self.startButton, 0, wx.ALL, 5)
        mainSizer.Add(self.log, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(mainSizer)

    def OnStartClick(self, e):
        if self.checking:
            self.workerThread.stop()
            self.checking = False
            return
        print self.mailInput.GetValue()
        dates = ['2013-05-01']
        cities = []
        cities.append(self.fromCityInput.GetValue())
        cities.append(self.toCityInput.GetValue())
        time_limit = [self.timeInputFrom.getValue(), self.timeInputTo.getValue()]
        email = self.mailInput.GetValue()
        ticket_t = self.typeCheckBoxGroup.getValue()
        train_c = self.classCheckBoxGroup.getValue()

        # print self.typeCheckBoxGroup.getValue()
        # print self.timeInputFrom.getValue() + "--" + self.timeInputTo.getValue()
        # print self.startDateCombo.getValue()

        self.workerThread = checker.Checker(dates, time_limit,
                                            cities, ticket_t, train_c, email, self)
        self.workerThread.start()
        self.checking = True

    def logging(self, msg):
        self.log.AppendText(msg+'\n')
