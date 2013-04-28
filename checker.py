# coding=utf-8
import urllib2
import re
import smtplib
import time
import threading
import wx
#######################################################
#Bugs here. The checker only checks the D and G train.#
#T,K and normal train need to be added.               #
#######################################################

ticket_type = [u'商务座', u'特等座', u'一等座', u'二等座',
               u'高级软卧', u'软卧', u'硬卧', u'软座', u'硬座', u'无座']


class Checker(threading.Thread):

    def __init__(self, train_date, time_limit, cities, selected_type, email_address, window):
        threading.Thread.__init__(self)
        self.dates = train_date
        self.time = time_limit
        self.cities = cities
        self.type = selected_type
        self.email_address = email_address
        self.window = window

    def run(self):
        while True:
            wx.CallAfter(self.window.logging, 'Start checking...')
            for date in self.dates:
                check_ticket(date, self.time, self.cities,
                             self.type, self.email_address, self.window.logging)
                # try:

                # except Exception, e:
                #     pass

            SHOW_MSG = 'CHECKED AT'
            ISOTIMEFORMAT = '%Y-%m-%d %X'
            s = SHOW_MSG + time.strftime(ISOTIMEFORMAT, time.localtime())
            wx.CallAfter(self.window.logging, s)
            wx.CallAfter(self.window.logging, 'Wait 30 seconds...')
            time.sleep(30)


def check_ticket(train_date, time_limit, cities, selected_type, email_address, logging):
    """
    Check function
    """
    timelimit_start = calc_time(time_limit[0][:2], time_limit[0][-2:])
    timelimit_end = calc_time(time_limit[1][:2], time_limit[1][-2:])
    # print cities[0].encode('utf-8')
    origin, dest = get_city_code(cities[0]), get_city_code(cities[1])

    query_url = 'http://dynamic.12306.cn/otsquery/query/queryRemanentTicketAction.do?method=queryLeftTicket&orderRequest.train_date=%s\
&orderRequest.from_station_telecode=%s&orderRequest.to_station_telecode=%s&orderRequest.train_no=&trainPassType=QB&trainClass=D%%23&\
includeStudent=00&seatTypeAndNum=&orderRequest.start_time_str=00%%3A00--24%%3A00' % (train_date, origin, dest)

    json_res = urllib2.urlopen(query_url).read()
    pattern = re.compile(r'<span id=.*?\\\\n|<span id=.*?"time"')
    item_list = pattern.findall(json_res)

    for item in item_list:
        num_pattern = re.compile(">(D|G|C)[0-9]+<")
        train_num_item = num_pattern.search(item)

        if train_num_item is None:
            continue

        train_num = train_num_item.group(0)[1:-1]

        time_pattern = re.compile("[0-9]{2}:[0-9]{2}")
        train_time = time_pattern.findall(item)

        time_thresh_value = calc_time(train_time[0][:2], train_time[0][-2:])

        if time_thresh_value < timelimit_start or time_thresh_value > timelimit_end:
            continue

        ticket_count_pattern = re.compile("--|<font color='darkgray'>|,[0-9]+")
        slist = ticket_count_pattern.findall(item)[1:]
        seat = [(t_type, slist[t_type])for t_type in selected_type]
        res = strip_comma(seat)

        if res != -1:
            # print train_date, train_num
            # print train_time
            # print seat
            tt = ticket_type[res]
            ticket_msg = u'日期: %s 车次: %s 席别: %s' % (train_date, train_num, tt)
            wx.CallAfter(logging, u"快抢票！" + ticket_msg)
            # send_mail_to(email_address, ticket_msg.encode('utf8'))

        else:
            wx.CallAfter(logging, "===" + train_num + "No Ticket ===")


def calc_time(hour, minute):
    return (int(hour))*60 + int(minute)


def strip_comma(seat_list):
    res = -1
    for index, item in seat_list:
        if item[0] == ',':
            res = True
            return index
    return res


def send_mail_to(mailto, ticket_msg):
    """
    Send mails to customers
    """
    mailfrom = 'train.ticket.archie@gmail.com'
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(mailfrom, 'ticketticket')

    header = 'To:' + mailto + '\n' + 'From: ' + mailfrom + \
        '\n' + 'Subject:FIND A TICKET FOR YOU !!!  ' + ticket_msg

    smtp.sendmail(mailfrom, mailto, header)
    smtp.quit()


# def input_date():
#     """
#     Enter the date
#     """
#     d = []
#     date = ''
#     while(True):
#         print u'输入日期（格式为(yyyy-mm-dd) ，每次一个，回车结束一次输入，输入END停止输入）'
#         date = raw_input()
#         if(date == 'END'):
#             break
#         while(len(date) != 10):
#             print u'输入错误，请注意格式\n'
#             print u'重新输入日期（格式为(yyyy-mm-dd) 输入END停止输入)'
#             date = raw_input()
#         d.append(date)

#     print u'所选日期:'
#     for adate in d:
#         print adate
#     return d


# def input_timelimit():
#     """
#     Enter the time limit
#     """
#     start_time = get_formatted_time(u'输入发车时间范围-开始时间:(hh:mm)')
#     end_time = get_formatted_time(u'输入发车时间范围-结束时间:(hh:mm)')
#     return start_time, end_time


# def get_formatted_time(s):
#     print s
#     time = raw_input()
#     while(len(time) != 5):
#         print '错误，请注意格式!'
#         time = raw_input(u'再次' + s)

#     return time


def get_city_code(city_name):
    """
    Transform city name into telecode
    """
    req = urllib2.Request('http://dynamic.12306.cn/otsquery/js/common\
/station_name.js?version=1.40')
    city_list = urllib2.urlopen(req).read()
    # print city_list.decode('utf8').encode('gbk')

    city_name = city_name.encode('utf8')
    city_rx = re.compile('\|'+city_name + '\|.+?\|')
    city_code = city_rx.search(city_list).group(0)[-4:-1]
    return city_code


# def input_cities():
#     """
#     Enter the city names
#     """
#     print u'出发地: '
#     origin = get_city_code(raw_input())
#     print u'目的地:'
#     dest = get_city_code(raw_input())
#     return origin, dest


# def input_email():
#     print u'请输入Email地址:'
#     return raw_input()


# def to_int(num_string):
#     return int(num_string)


# def input_tickettype():
#     print u'请输入车票类型编码(可同时输入多个): '
#     i = 0
#     for t in ticket_type:
#         print i, t
#         i += 1
#     s = raw_input()
#     num_pattern = re.compile('[0-9]')
#     g = map(to_int, num_pattern.findall(s))
#     return g

# if __name__ == '__main__':
#     dates = input_date()
#     cities = input_cities()
#     time_limit = input_timelimit()
#     email = input_email()
#     ticket_t = input_tickettype()
# dates = ['2013-04-19']
# cities = ['']
# time_limit = ['00:00', '23:23']
# email = 'archieyang@foxmail.com'
# ticket_t = [0, 2, 3]
#     while True:
#         print 'Start checking...'
#         for date in dates:
#             check_ticket(date, time_limit, cities, ticket_t, email)
# try:

# except Exception, e:
# pass

#         SHOW_MSG = 'CHECKED AT'
#         ISOTIMEFORMAT = '%Y-%m-%d %X'
#         print SHOW_MSG, time.strftime(ISOTIMEFORMAT, time.localtime())
#         print 'Wait 30 seconds...'
#         time.sleep(30)
