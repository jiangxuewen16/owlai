from app import app
from core import utils, config

from core import dbengine


@app.route('/')
def hello_world():
    print(dir(dbengine))
    return {"name": config.get_config("APP_NAME"), "age": 12}