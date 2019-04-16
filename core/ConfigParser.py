import configparser
import os

"""
读取配置文件信息
"""

class ConfigParser():

    config_file = os.path.abspath(os.path.dirname(__file__))+'\\core.config'
    config_dic = {}
    @classmethod
    def get_config(cls, sector, item):
        value = None
        try:
            value = cls.config_dic[item]
        except KeyError:
            cf = configparser.ConfigParser()
            cf.read(cls.config_file, encoding='utf8')
            value = cf.get(sector, item)
            cls.config_dic[item] = value
        finally:
            return value