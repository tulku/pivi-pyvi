from configuration import Configuration
import logging
import logging.handlers


def get_logger(name, conf_file='/etc/pivi.cfg', max_bytes=10240,
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
