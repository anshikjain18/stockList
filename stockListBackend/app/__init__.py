import logging
import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_swagger_ui import get_swaggerui_blueprint

logger = logging.getLogger(__name__)


def create_app():
    configure_logger()
    app = Flask(__name__)

    logger.info("Flask app initialized.")

    load_dotenv()
    configure_mongodb(app)
    configure_cors(app)
    configure_jwt(app)
    configure_swagger(app)
    configure_blueprints(app)

    return app


def configure_logger():
    logging.basicConfig(level=logging.INFO)
    logger.info('Logger is configured.')


def configure_mongodb(app):
    app.config['MONGODB_SETTINGS'] = {
        "host": os.getenv('MONGO_DB_URI')
    }
    MongoEngine(app)
    logger.info("mongodb connected.")


def configure_cors(app):
    CORS(app, origin=[os.getenv('STOCKLIST_UI_URL'), os.getenv('STOCKLIST_API_URL')])


def configure_jwt(app):
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(weeks=1)
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    jwt = JWTManager(app)
    logger.info("JWT manager initialized.")


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        from .auth import BLOCKLIST
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )


def configure_swagger(app):
    @app.route('/swagger/')
    def swagger():
        return open('static/swagger.yml').read()

    swagger_url = '/api/docs'
    api_url = '/swagger'

    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={'app_name': 'StockList'}
    )
    app.register_blueprint(swaggerui_blueprint)
    logger.info("Swagger UI initialized.")


def configure_blueprints(app):
    """
    method to register different blueprints to the flask app
    :param app: Flask application
    """
    from . import views, auth

    app.register_blueprint(views.views, url_prefix='/')
    app.register_blueprint(auth.auth, url_prefix='/auth')
    logger.info("Blueprints are registered.")
