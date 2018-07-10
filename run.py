import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from app import app

if __name__ == '__main__':
    handler = RotatingFileHandler(filename='./log/app.log', maxBytes=1048576, backupCount=3)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    default_handler.setLevel(logging.INFO)
    app.logger.addHandler(default_handler)

    app.run(host='0.0.0.0', port=9000)
