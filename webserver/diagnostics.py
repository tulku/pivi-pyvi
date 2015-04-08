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
        web.header("Content-Disposition", "attachment; filename=pivi-logs.zip")
        web.header('Content-Type', 'application/zip')
        timestamp = time.ctime(time.time())
        lr.zip_logs()
        path = '/tmp/pivi-logs.zip'
        try:
            f = open(path, 'r')
            return f.read()
        except:
            return render.sendmail("ERROR, no zip file generated", timestamp)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
