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

    """ # flask.logging.create_logger
    logger = logging.getLogger('flask.app')

    if app.debug and logger.level == logging.NOTSET:
        logger.setLevel(logging.DEBUG)

    if not has_level_handler(logger):
        logger.addHandler(default_handler)

    return logger
    """
    default_handler.setLevel(logging.INFO)
    app.logger.addHandler(default_handler)

    app.run(host='0.0.0.0', port=9000)
