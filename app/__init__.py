from flask import Flask
from .utils import *


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

from .views import *
