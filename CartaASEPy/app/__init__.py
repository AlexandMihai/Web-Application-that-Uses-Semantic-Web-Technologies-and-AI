from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_session import Session
import psycopg2
import logging

mail = Mail()
jwt = JWTManager()
sess = Session()


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    app.secret_key = '6098038a18833fd04104337475f13351'

    CORS(app, supports_credentials=True,
         resources={r"/*": {"origins": ["http://127.0.0.1:5000", "http://localhost:5000"]}})

    # Mail
    app.config['MAIL_SERVER'] = 'smtp.office365.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = '-@outlook.com'
    app.config['MAIL_PASSWORD'] = '-'
    app.config['MAIL_DEFAULT_SENDER'] = '-@outlook.com'
    mail.init_app(app)

    app.config['JWT_SECRET_KEY'] = '-'
    jwt.init_app(app)

    # Session Configuring
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    sess.init_app(app)

    # Database Connection
    app.config['DATABASE'] = {
        'dbname': "ASE",
        'user': "ASE",
        'password': "ASE",
        'host': "localhost",
        'port': "5432"
    }

    with app.app_context():
        from .auth import routes as auth_routes
        from .chat import routes as chat_routes
        from . import routes as main_routes

        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(chat_routes.bp)
        app.register_blueprint(main_routes.bp)

    logging.basicConfig(level=logging.DEBUG)

    return app
