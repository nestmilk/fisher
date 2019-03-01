from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from app.models.base import db

login_manager = LoginManager()
mail= Mail()

def create_app():
    app = Flask(__name__)
    #替代from config import DEBUG
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'
    db.create_all(app=app)

    mail.init_app(app)
    return app


def register_blueprint(app):
    from app.web.blueprint import web
    app.register_blueprint(web)