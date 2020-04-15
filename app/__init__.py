# _*_ Coding:utf-8 _*_

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    # 注册web服务蓝图
    from app.services import services as service_blueprint
    # url_prefix='/services'
    app.register_blueprint(service_blueprint)

    return app



