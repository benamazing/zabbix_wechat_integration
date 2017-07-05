#!/usr/bin/env python

import tornado.web
import tornado.httpserver
from tornado.options import define, options
import itchat
import os

from config import *


# init login and get the distribution list
itchat.auto_login(hotReload=True, picDir='/usr/share/nginx/html/QR.png')

with open('recipients.conf') as f:
    for line in f:
        if line.startswith('users='):
            user_list = line[line.find('=')+1:].strip('\r\n').split(',')
        if line.startswith('groups='):
            group_list = line[line.find('=')+1:].strip('\r\n').split(',')

wechat_user_list = []
for user in user_list:
    if user != '':
        results = itchat.search_friends(name=user)
        for x in results:
            wechat_user_list.append(x)

wechat_group_list = []
for group in group_list:
    if group != '':
        results = itchat.search_chatrooms(name=group)
        for x in results:
            wechat_group_list.append(x)

for user in wechat_user_list:
    userId = user[u'UserName']
    itchat.send(u'Hello, alert sender is running!', toUserName=userId)

for user in wechat_group_list:
    userId = user[u'UserName']
    itchat.send(u'Hello, alert sender is running!', toUserName=userId)

define("listen_port", default=8082, help="run on the given port", type=int)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers,template_path=os.path.join(os.path.dirname(__file__), "templates"),static_path=os.path.join(os.path.dirname(__file__), "static"))
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.listen_port)
    print ('Start listening on port %s' % options.listen_port)
    tornado.ioloop.IOLoop.instance().start()
