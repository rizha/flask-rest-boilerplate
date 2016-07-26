import logging

from flask import Flask
from extensions import mongo, cache, celery
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from api import api_bp as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api')

    mongo.init_app(app)
    cache.init_app(app)
    celery.conf.update(app.config)

    if app.debug is False:
        log_folder_path = app.config.root_path + '/../logs/'

        log_file = {
            'file': log_folder_path + 'default.log'
        }

        file_handler = logging.FileHandler(log_file['file'])
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

    return app

