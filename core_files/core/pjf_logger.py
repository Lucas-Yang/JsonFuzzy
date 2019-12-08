#! /usr/bin/env python
# -*- encoding:utf-8 -*-
# ylucas923@163.com
###########################################
from .pjf_version import PYJFUZZ_LOGLEVEL
import logging
import os
import time
import sys


filename = 'log/fuzzer_{0}.log'.format(time.strftime("%d_%m_Y"))
dir = os.path.dirname(filename)
if not os.path.isdir(dir):
    os.mkdir(dir)


class PJFLogger(object):

    @staticmethod
    def init_logger():
        logging.basicConfig(filename="log/fuzzer_{0}.log".format(time.strftime("%d_%m_%Y")),
                            level=PYJFUZZ_LOGLEVEL, datefmt="%H:%M:%S")
        logger = logging.getLogger(__name__)
        sys.exc_traceback = 10

        def handle_exception(exc_type, exc_value, exc_traceback):
            """
            :exception
            :param exc_type:
            :param exc_value:
            :param exc_traceback:
            :return:
            """
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
            sys.__excepthook__(exc_type, exc_value, None)
            return

        sys.excepthook = handle_exception
        return logger
