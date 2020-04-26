# _*_ Coding:utf-8 _*_

from flask import Blueprint
from app.services.interface import *
from app.services.business_interface import *

services = Blueprint("services", __name__)

serviceDict = {
                "1": edit_register,
                "2": query_register,
                "256": edit_vehicle,
                "257": query_vehicle,
                "258": edit_vehicletype,
                "259": query_vehicletype,
                "260": edit_graintype,
                "261": query_graintype,
                "262": edit_packtype,
                "263": query_packtype,
                "264": edit_paymenttype,
                "265": query_paymenttype,
                "266": edit_sampleclass,
                "267": query_sampleclass,
                "268": edit_banktype,
                "269": query_banktype,
                "270": edit_warehouse,
                "271": query_warehouse,
                "272": edit_transport,
                "273": query_transport,
                "274": edit_supplier,
                "275": query_supplier,
                "276": edit_contracttype,
                "277": query_contracttype,
                "278": edit_purchase,
                "279": query_purchase,
                "280": edit_procedurenode,
                "281": query_procedurenode,
                "282": edit_seller,
                "283": query_seller,
                "284": edit_contract,
                "285": query_contract,
                "290": edit_valuation,
                "291": query_valuation,
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



