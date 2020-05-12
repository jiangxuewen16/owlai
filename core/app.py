import os

import yaml

from core import config
from core.utils import auto_import_module
from core import dbengine


class App(object):
    BASE_CONFIG = "config"
    BASE_SCHEDULER = "scheduler"
    CONFIG_EXT = ".yml"

    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def run(self, env: str):
        # 根据环境引入配置
        self.init_config(env)
        # 引入常用包
        self.add_package()
        # 数据库引擎
        self.add_engine()

    def add_package(self):
        auto_import_module(self.BASE_SCHEDULER)  # 业务代码写到此包中

    def add_engine(self):
        print(config.CONFIG.items())
        for key, value in config.CONFIG.items():
            if hasattr(dbengine, key):
                attr = getattr(dbengine, key)
                attr(value)

    def init_config(self, env: str):
        """
        初始化配置
        :param env: 环境变量
        :return:
        """
        config_path = os.path.join(self.base_dir, self.BASE_CONFIG)

        listdir = os.listdir(config_path)
        for item in listdir:
            new_path = os.path.join(config_path, item)
            if not os.path.isdir(new_path) and os.path.splitext(new_path)[1] == self.CONFIG_EXT and env in \
                    os.path.splitext(new_path)[0]:
                with open(new_path, encoding='utf-8') as f:
                    res = yaml.load(f, Loader=yaml.FullLoader)
                    for key, value in res.items():
                        config.CONFIG[key] = value
