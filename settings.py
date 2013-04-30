# coding=utf-8
import json


class info(object):
    dates = 'dates'
    time_limit = 'time'
    cities = 'cities'
    ticket_type = 'ticket_t'
    train_class = 'train_c'
    email = 'email'
    """docstring for info"""
    def __init__(self, dates=None, time_limit=None,
                 cities=None, ticket_t=None, train_c=None, email=None):
        super(info, self).__init__()

        self.dates = dates
        self.time_limit = time_limit
        self.cities = cities
        self.ticket_t = ticket_t
        self.train_c = train_c
        self.email = email

    def save(self):
        dict_to_json = {}
        dict_to_json[info.dates] = self.dates
        dict_to_json[info.time_limit] = self.time_limit
        dict_to_json[info.cities] = self.cities
        dict_to_json[info.ticket_type] = self.ticket_t
        dict_to_json[info.train_class] = self.train_c
        dict_to_json[info.email] = self.email
        print json.dumps(dict_to_json)
        try:
            with open('config', 'w') as config:
                config.write(json.dumps(dict_to_json))
        except Exception, e:
            raise e

    def load(self):
        dict_to_json = {}
        try:
            with open('config', 'r') as config:
                dict_to_json = json.loads(config.read())
        except Exception, e:
            raise e

        self.dates = dict_to_json[info.dates]
        self.time_limit = dict_to_json[info.time_limit]
        self.cities = dict_to_json[info.cities]
        self.ticket_t = dict_to_json[info.ticket_type]
        self.train_c = dict_to_json[info.train_class]
        self.email = dict_to_json[info.email]
