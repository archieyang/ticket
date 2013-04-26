# coding=utf-8
import wx
import checker


class MPanel(wx.Panel):

    """docstring for ClassName"""
    def __init__(self, parent):
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
        self.dateInput = wx.TextCtrl(self, size=(140, -1))
        dateBox.Add(self.dateLabel)
        dateBox.Add(self.dateInput)

        timeBox = wx.BoxSizer(wx.HORIZONTAL)
        self.timeLabel = wx.StaticText(self, label=time)
        self.timeInputFrom = wx.TextCtrl(self, size=(140, -1))
        self.timeInputTo = wx.TextCtrl(self, size=(140, -1))
        timeBox.Add(self.timeLabel)
        timeBox.Add(self.timeInputFrom)
        timeBox.Add(self.timeInputTo)

        ticket_type = [u'商务座', u'特等座', u'一等座', u'二等座',
                       u'高级软卧', u'软卧', u'硬卧', u'软座', u'硬座', u'无座']
        seatBox = wx.RadioBox(self, label=seat, choices=ticket_type,
                              majorDimension=5)

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
        mainSizer.Add(seatBox, 0, wx.ALL, 5)
        mainSizer.Add(mailBox, 0, wx.ALL, 5)
        mainSizer.Add(self.startButton, 0, wx.ALL, 5)
        mainSizer.Add(self.log,1, wx.EXPAND|wx.ALL, 5)

        self.SetSizerAndFit(mainSizer)

    def OnStartClick(self, e):
        print self.mailInput.GetValue()
        dates = ['2013-04-30']
        cities = []
        cities.append(self.fromCityInput.GetValue())
        cities.append(self.toCityInput.GetValue())
        time_limit = ['00:00', '23:23']
        email = 'archieyang@foxmail.com'
        ticket_t = [0, 2, 3]
        workerThread = checker.Checker(dates, time_limit,
                                       cities, ticket_t, email, self)
        workerThread.start()

    def logging(self, msg):
        self.log.AppendText(msg+'\n')
