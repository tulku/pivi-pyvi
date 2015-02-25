#!/usr/bin/env python

import web
import time

from utils import logs
from utils import Configuration

render = web.template.render('templates/')

urls = ('/', 'index',
        '/sendlogs(.*)', 'sendlogs')

conf = Configuration()
lr = logs.LogReader()
LOG_LEVEL = conf.log_level()
LOG_MAIL = conf.log_mail()


class index(object):
    """ Main web page. """

    def GET(self):
        timestamp = time.ctime(time.time())
        logs_names, logs_cont = lr.get_logs()
        return render.index(LOG_LEVEL, logs_names, logs_cont, timestamp)


class sendlogs(object):

    def GET(self, *args):
        timestamp = time.ctime(time.time())
        lr.send_mail()
        return render.sendmail(LOG_MAIL, timestamp)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
