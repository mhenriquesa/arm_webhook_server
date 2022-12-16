from flask import Flask
from src.Config import Config
import sys
import logging


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

    from src.routes import main
    app.register_blueprint(main)

    return app
