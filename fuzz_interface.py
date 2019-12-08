#! /usr/bin/env python
# -*- encoding:utf-8 -*-
# ylucas923@163.com
###########################################
"""
fuzzy工具层接口文件
"""

import abc
import codecs
import json
import sys

# import core lib
from argparse import Namespace
from core_files.lib import *

class FuzzyApiBase(object):
    """
    接口抽象类
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def fuzz_data(self, template_dict, fuzz_type):
        """实时返回数据
        :param template_dict: 用户传入json数据，该函数会fuzz全部key对应的value
        :param fuzz_type: 生成特殊字符串选项，一共有七个选项，["X", "H", "S", "T", "C", "L", "R"],
                         分别代表[xss注入, http header注入, SQL注入, 模板注入, RCE注入, LFI攻击
                         , 随机串] 如果都不选，代表都选择
        :return: dict, fuzz后的数据
        """
        pass

    @abc.abstractmethod
    def fuzz_file(self, template_dict, fuzz_type, case_num, file_name):
        """批量生成数据保存到文件
        :param template_dict:
        :param fuzz_type:
        :param case_num: 生成数据量
        :param file_name: 保存文件名
        """
        pass


class FuzzyApi(FuzzyApiBase):
    """
    接口层
    """
    def fuzz_data(self, template_dict, fuzz_type=""):
        """调用该接口生成fuzz后的数据
        :param template_dict:
        :param fuzz_type:
        :return:
        """
        if (not isinstance(template_dict, dict)) or (not template_dict):
            raise Exception("Invalid dict template", template_dict)
        elif (not isinstance(fuzz_type, str)) or (fuzz_type not in ["X", "H", "S", "T", "C", "L", "R", ""]):
            raise Exception("Invalid fuzz_type", fuzz_type)
        else:
            config = PJFConfiguration(Namespace(json=template_dict, nologo=True, level=6, techniques=fuzz_type))
            fuzzer = PJFFactory(config)
            return_data = json.loads(fuzzer.fuzzed)
            return return_data

    def fuzz_file(self, template_dict, fuzz_type="", case_num=1000, file_name="result/fuzz_result.json"):
        """
        :param template_dict:
        :param fuzz_type:
        :param case_num:
        :param file_name:
        :return:
        """
        if (not isinstance(template_dict, dict)) or (not template_dict):
            raise Exception("Invalid dict template", template_dict)
        elif (not isinstance(fuzz_type, str)) or (fuzz_type not in ["X", "H", "S", "T", "C", "L", "R", ""]):
            raise Exception("Invalid fuzz_type", fuzz_type)
        elif (not isinstance(case_num, int)) or (case_num < 0):
            raise Exception("Invalid case_num", case_num)
        elif (not isinstance(file_name, str)):
            raise Exception("Invalid file_name", file_name)
        else:
            config = PJFConfiguration(Namespace(json=template_dict, nologo=True, level=6, techniques=fuzz_type))
        result_list = []
        fuzzer = PJFFactory(config)
        for i in range(case_num):
            result_list.append(json.loads(fuzzer.fuzzed))
        try:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                json.dump(result_list, f, ensure_ascii=False)
        except Exception as error:
            raise Exception("Write json file error", error)


if __name__ == "__main__":
    fuzzer = FuzzyApi()
    json_data = {
        "name": "小明"
    }
    result_data = fuzzer.fuzz_data(json_data, fuzz_type="")
    print(result_data)


