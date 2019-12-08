#! /usr/bin/env python
# -*- encoding:utf-8 -*-
# ylucas923@163.com
###########################################

import os
import sys
import json
import logging

from argparse import Namespace
from .pjf_logger import PJFLogger

class PJFConfiguration(Namespace):
    """config
    """
    def __init__(self, arguments):
        """init the command line
        :param arguments:
        """
        super(PJFConfiguration, self).__init__(**arguments.__dict__)
        try:
            if self.techniques:
                l_techniques = {
                    "C": [10, 5, 13],
                    "H": [9],
                    "L": [6, 2, 8],
                    "T": [11, 12],
                    "R": [14],
                    "S": [3, 1],
                    "X": [0, 4, 7]
                }
                temp = []
                for technique in self.techniques:
                    if technique in l_techniques:
                        temp += l_techniques[str(technique)]
                self.techniques = temp
            else:
                self.techniques = list(range(0, 14))
            self.parameters = []
            self.command = ['echo']
            self.utf8 = False
            self.stdin = True
            self.strong_fuzz = False
            self.url_encode = False
            self.indent = False
        except Exception as error:
            raise Exception(error)
