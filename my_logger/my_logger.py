import logging


def mylogger(_logname: str = 'mylog', _screen=True, _file=None,
             _screen_fmt: str = None, _file_fmt: str = None,
             _screen_level: str = None, _file_level: str = None):
    _logger = logging.getLogger(_logname)
    _logger.setLevel(logging.DEBUG)

    _level = {'debug': logging.DEBUG, 'DEBUG': logging.DEBUG,
              'info': logging.INFO, 'INFO': logging.INFO,
              'warn': logging.WARN, 'WARN': logging.WARN,
              'warning': logging.WARNING, 'WARNING': logging.WARNING,
              'error': logging.ERROR, 'ERROR': logging.ERROR,
              'critical': logging.CRITICAL, 'CRITICAL': logging.CRITICAL}

    if _screen:
        screen_handler = logging.StreamHandler()

        if _screen_fmt is None:
            _screen_fmt = '%(asctime)s line:%(lineno)d %(levelname)s %(message)s'
        date_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(_screen_fmt, date_fmt)
        screen_handler.setFormatter(formatter)

        if _screen_level is None:
            _screen_level = 'debug'
        screen_handler.setLevel(_level[_screen_level])

        _logger.addHandler(screen_handler)
    if _file:
        file_hander = logging.FileHandler(_file, encoding='utf8')

        if _file_fmt is None:
            _file_fmt = '%(asctime)s line:%(lineno)d %(levelname)s %(message)s'
        date_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(_file_fmt, date_fmt)
        file_hander.setFormatter(formatter)

        if _file_level is None:
            _file_level = 'debug'
        file_hander.setLevel(_level[_file_level])

        _logger.addHandler(file_hander)

    return _logger


if __name__ == '__main__':
    logger = mylogger(_file='log.txt', _file_level='INFO')
    logger.debug('就是这样')
    logger.info('这是info')
    logger.error('这是error')
    logger.warning('WARING!!!')
