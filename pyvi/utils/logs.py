# This file is part of the Pyvi software package. Released
# under the Creative Commons ATT-NC-ShareAlire license
# http://creativecommons.org/licenses/by-nc-sa/4.0/
# Copyright (C) 2014, 2015 LESS Industries S.A.
# Lucas Chiesa <lucas@lessinduestries.com>


from configuration import Configuration
import logging
import logging.handlers
import re
import os
import smtplib
import zipfile
import errno
from os.path import isfile, join

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


def get_logger(name, conf_file='/etc/pivi.cfg', max_bytes=10240*10,
               max_backup=5):
    """
    Gets a logger instance with a desired name and the log level
    configured in the system configuration.

    :param name: The name that wants to be used in the logs.
    :type name: string
    :param conf_file: The configuration file to use.
        Defaults to system configuration
    :type conf_file: string
    :param max_bytes: the max number of bytes for each file
    :type max_bytes: int
    :param max_backup: the max number of old copies of the file
    :type max_backup: int
    :returns: a logger
    """
    conf = Configuration(conf_file).log_level()
    log_dir = Configuration(conf_file).log_dir()
    destfile = log_dir + '/' + name + '.log'

    if conf == 'debug':
        level = logging.DEBUG
    if conf == 'info':
        level = logging.INFO
    if conf == 'warning':
        level = logging.WARNING
    if conf == 'error':
        level = logging.ERROR
    if conf == 'critical':
        level = logging.CRITICAL

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # add a file handler
    fh = logging.handlers.RotatingFileHandler(destfile, mode='a',
                                              maxBytes=max_bytes,
                                              backupCount=max_backup)
    fh.setLevel(level)
    # create a formatter and set the formatter for the handler.
    frmt = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    fh.setFormatter(frmt)
    # add the Handler to the logger
    logger.addHandler(fh)

    return logger


class LogReader(object):

    def __init__(self, conf_file='/etc/pivi.cfg'):
        self.conf_file = conf_file
        self.conf = Configuration(self.conf_file)
        self.log_dir = self.conf.log_dir()
        self.log_mail = self.conf.log_mail()
        self.pivi_id = self.conf.pivi_id()

    def _filter_logs(self, filename):
        test1 = re.match('.*\.log$', filename)
        test2 = isfile(join(self.log_dir, filename))
        return all([test1, test2])

    def _get_file(self, file_name):
        try:
            full = join(self.log_dir, file_name)
            with open(full, 'r') as in_file:
                contents = in_file.read()
        except IOError:
            contents = None
        return contents

    def _get_log_files(self):
        plain = [f for f in os.listdir(self.log_dir) if self._filter_logs(f)]
        return plain

    def _silentremove(self, filename):
        """
        Delete a file if it existed. Do nothing if it does not exist.
        Raise exceptions in other cases.
        """
        try:
            os.remove(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def _zip_logs(self):
        zipname = '/tmp/pivi-logs.zip'
        self._silentremove(zipname)
        out = zipfile.ZipFile(zipname, 'w')
        for root, dirs, files in os.walk(self.log_dir):
            for file_name in files:
                out.write(os.path.join(root, file_name))
        out.close()

    def get_logs(self):
        logs_cont = []
        logs_names = self._get_log_files()
        for log in logs_names:
            cont = self._get_file(log)
            if cont is not None:
                logs_cont.append(cont)
            else:
                logs_cont.append('Could not be opened.')

        return logs_names, logs_cont

    def send_mail(self, msg=""):
        if not self.conf.send_email():
            return
        self._zip_logs()
        send_to = [self.log_mail]
        send_from = 'pivi.logs.reporter@gmail.com'
        files = ['/tmp/pivi-logs.zip', self.conf_file]
        subject = 'Pivi Logs for ID ' + str(self.pivi_id)
        text = "These are the collected logs of a Pivi in trouble!"
        text += '\n\n' + msg
        username = send_from
        password = 'pivi.logs'

        assert type(send_to) == list
        assert type(files) == list

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)

        server.sendmail(send_from, send_to, msg.as_string())
        server.close()
