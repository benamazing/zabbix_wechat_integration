# -*- coding: utf-8 -*-

import tornado.web
from main import wechat_group_list
from main import wechat_user_list
import itchat
import datetime


class AlertHandler(tornado.web.RequestHandler):
    def get(self):
        message = self.get_argument('message', '')
        type = self.get_argument('type', '')
        try:
            self.send_alert_to_wechat(type, message)
            self.write('%s: Send to Wechat group successfully!' % datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
        except Exception, e:
            self.write('%s: Failed to send alert to wechat group! %s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), e))

    def post(self):
        self.get()

    def send_alert_to_wechat(self, type, message):
        for group in wechat_group_list:
            itchat.send('[%s]: %s' % (type, message), toUserName=group[u'UserName'])
        for user in wechat_user_list:
            itchat.send('[%s]: %s' % (type, message), toUserName=user[u'UserName'])


