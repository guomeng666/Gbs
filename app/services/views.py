# _*_ coding:utf-8 _*_
from app import db
from . import services
from flask import render_template, redirect, url_for, flash, session, request, jsonify
import json
from sqlalchemy import or_, func, and_
from sqlalchemy.sql.elements import FunctionFilter
from functools import wraps


@services.route("/", methods=["POST", "GET"])
def index():
    # data = request.form.get('User')
    user = request.json.get("User")
    password = request.json.get("Password")
    image = request.json.get("Image")
    print("User:", user)
    print("Password:", password)
    print("image:", image)
    return image
