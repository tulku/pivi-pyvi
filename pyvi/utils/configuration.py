# This file is part of the Pyvi software package. Released
# under the Creative Commons ATT-NC-ShareAlire license
# http://creativecommons.org/licenses/by-nc-sa/4.0/
# Copyright (C) 2014, 2015 LESS Industries S.A.
# Lucas Chiesa <lucas@lessinduestries.com>


import ConfigParser
import os


class Configuration(object):

    def __init__(self, conf_file='/etc/pivi.cfg'):
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(conf_file))

    def _bool(self, val):
        return val.lower() == 'true'

    def is_virtual(self):
        return self._bool(self.config.get('general', 'virtual'))

    def send_email(self):
        return self._bool(self.config.get('logs', 'send_email'))

    def server_uri(self):
        address = self.config.get('server', 'address').lower()
        port = self.config.get('server', 'Port').lower()
        return {'address': address, 'port': port}

    def serial_port(self):
        port = self.config.get('serial', 'device')
        baudrate = int(self.config.get('serial', 'baudrate'))
        timeout = float(self.config.get('serial', 'timeout'))
        return {'port': port, 'baudrate': baudrate,
                'timeout': timeout}

    def pivi_id(self):
        id_ = int(self.config.get('general', 'id'))
        if self.is_virtual():
            id_ = 0
        return id_

    def log_level(self):
        return self.config.get('logs', 'level').lower()

    def log_dir(self):
        directory = self.config.get('logs', 'dir').lower()
        try:
            os.makedirs(directory)
            # User and Group of the default first user in debian systems
            os.chown(directory, 1000, 100)
        except OSError:
            pass
        return directory

    def log_mail(self):
        mail = self.config.get('logs', 'mail').lower()
        return mail
