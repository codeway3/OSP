from flask import Flask

app = Flask(__name__, instance_relative_config=True)

try:
    app.config.from_pyfile('config.py')
except FileNotFoundError:
    pass

from .views import *
from .utils import *
