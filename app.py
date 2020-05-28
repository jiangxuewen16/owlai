import os
from flask import Flask
from core.app import App
from core.utils import auto_import_module

# os.environ['JAVA_HOME'] = 'C:\Program Files\Java\jdk1.8.0_251'
# os.environ['JAVA_HOME'] = '/System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands'
# os.environ['PYSPARK_PYTHON'] = '/Library/Frameworks/Python.framework/Versions/3.7'
os.environ['PYSPARK_PYTHON'] = '/usr/local/bin/python3.7'
os.environ['HADOOP_USER_NAME'] = 'hadoop'
# os.environ['HADOOP_CONF_DIR'] = '/usr/local/hadoop/etc/hadoop'
# os.environ['HADOOP_CLASSPATH'] = '/usr/local/hadoop:/usr/local/hbase/lib/*'

app = Flask(__name__)

# 这里放每个应用的视图包，自动加载，主要用于自定路径路由注册
auto_import_module('scheduler')  # view包，业务代码写到此包中

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "owlai")

# test develop production
env = os.getenv('FLASK_ENV') if not os.getenv('FLASK_ENV') else "test"
App(BASE_DIR).run(env)

if __name__ == '__main__':
    app.run()


