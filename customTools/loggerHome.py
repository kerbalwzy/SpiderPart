# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 60
import os
import logging
import datetime


class _MyLoggerMaker(object):
    """this is a logger maker class, to use function 'create_logger' you will get a special logger
        when this logger work ,it will create the dir by the primary 'name' you send in.
        the log file name is define by date auto and the primary 'name'.
        last ,we don't support console printer. just file writer.
    """

    def __init__(self):
        """ there is the config information ,after you create an object you can also change it
            by self.attribute name. And then through by function 'create_logger',you can get the
            logger you need.
        """
        self.level = logging.INFO
        self.format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        self.datefmt = '%a, %d %b %Y %H:%M:%S'
        self.filemode = 'w'

    def _create_logger(self, name):
        """
        this is a function to help you get a logger you need.
        :param name:
        :return:logger object
        """
        date = datetime.date.today()
        log_dir = os.path.dirname(os.path.dirname(__file__)) + '/logs/{}'.format(name)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_path = os.path.join(log_dir, '{}:{}.log'.format(name, date))
        # print(log_path)
        # create logger handler to achieve write different log information into different log file
        handler = logging.FileHandler(log_path)
        logging.basicConfig(level=self.level,
                            format=self.format,
                            datefmt=self.datefmt,
                            # filename=log_path,
                            filemode=self.filemode)
        handler_format = logging.Formatter(fmt=self.format, datefmt=self.datefmt)
        handler.setFormatter(handler_format)

        logger = logging.getLogger(name)
        # add handler into logger
        logger.addHandler(handler)
        return logger


_maker = _MyLoggerMaker()

videologger = _maker._create_logger("video")
musiclogger = _maker._create_logger("music")
novellogger = _maker._create_logger("novel")


if __name__ == '__main__':
    # maker = MyLoggerMaker()
    # mylogger = maker.create_logger("default")
    # mylogger.info("xixixixxi")
    pass
