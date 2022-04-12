# -*- coding: utf-8 -*-
"""
加载配置信息
"""
import yaml

# def loadCFG():
#     f = open('../config.yaml', 'r')
#     data = yaml.safe_load(f)
#     print(data)
#     return data

_global_dict={}

def _init():  # 初始化
    global _global_dict
    f = open('../config.yaml', 'r')
    _global_dict = yaml.safe_load(f)
    print(_global_dict)

def get():
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict
    except KeyError:
        print()