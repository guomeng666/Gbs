# _*_ Coding:utf-8 _*_

from flask import Blueprint

services = Blueprint("services", __name__)

# 这里需要导入视图,不加这一句的会无法找到路由
import app.services.views

