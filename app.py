import os
from flask import Flask
from core.app import App
from core.utils import auto_import_module

app = Flask(__name__)

# 这里放每个应用的视图包，自动加载，主要用于自定路径路由注册
# auto_import_module('scheduler')  # view包，业务代码写到此包中

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "owlai")

# test develop production
env = os.getenv('FLASK_ENV') if not os.getenv('FLASK_ENV') else "test"
App(BASE_DIR).run(env)

if __name__ == '__main__':
    app.run()

