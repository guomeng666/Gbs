# _*_ Coding:utf-8 _*_

from flask import Blueprint
from app.services.interface import *

services = Blueprint("services", __name__)

serviceDict = {"504": query_role}

# 这里需要导入视图,不加这一句的会无法找到路由
import app.services.views



