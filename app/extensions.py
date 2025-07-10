from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
import logging

mongo = PyMongo()
jwt = JWTManager()
ma = Marshmallow()

class AppLogger:
    def __init__(self):
        self.logger = logging.getLogger('hookaba')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    def init_app(self, app):
        app.logger.handlers = self.logger.handlers
        app.logger.setLevel(self.logger.level)

logger = AppLogger() 