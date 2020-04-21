# _*_ Coding:utf-8 _*_

from flask import Blueprint
from app.services.interface import *

services = Blueprint("services", __name__)

serviceDict = {
                "258": edit_vehicletype,
                "259": query_vehicletype,
                "501": edit_department,
                "502": query_department,
                "503": edit_role,
                "504": query_role,
                "505": edit_user,
                "506": query_user,
                "507": edit_permission,
                "508": query_permission
               }

# 这里需要导入视图,不加这一句的会无法找到路由
import app.services.views



