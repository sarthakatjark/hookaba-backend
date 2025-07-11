import os
from flask import Flask
from .config import get_config
from .extensions import mongo, jwt, ma, logger
from .auth import auth_bp
from app.users.routes import users_bp
from flasgger import Swagger
from app.library import library_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # Load .env if present
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
    #print('MONGO_URI from env:', os.environ.get('MONGO_URI'))
    # Load default config
    app.config.from_object(get_config())
    # Load instance config if exists
    app.config.from_pyfile('config.py', silent=True)
    #print('MONGO_URI from app.config:', app.config.get('MONGO_URI'))
    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    logger.init_app(app)
    Swagger(app)
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp)
    app.register_blueprint(library_bp)
    return app 