# _*_ coding:utf-8 _*_
from app import db
from . import services, serviceDict
from flask import render_template, redirect, url_for, flash, session, request, jsonify
import json
from sqlalchemy import or_, func, and_
from sqlalchemy.sql.elements import FunctionFilter
from functools import wraps


@services.route("/query", methods=["POST", "GET"])
def index():
    # data = request.form.get('User')
    cmd = request.json.get("Cmd")
    print(cmd)
    if cmd is not None:
        handler = serviceDict.get(cmd)
        if handler:
            return handler()
    return "error"



