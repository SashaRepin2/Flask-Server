from flask import jsonify, make_response, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, unset_jwt_cookies, jwt_required, \
    get_jwt_identity, set_access_cookies
from werkzeug.utils import redirect

from ..email import send_email

from ..models import *
from . import api, controller

#
# @api.route("/auth/registration", methods=['POST'])
# def auth_register():
#     return controller.auth_register()
#
#
# @api.route("/auth/login", methods=['POST'])
# def auth_login():
#     return controller.auth_login()
#
#
# @api.route("/auth/logout", methods=['POST'])
# def user_logout():
#     response = jsonify({"msg": "Logout is success"})
#     unset_jwt_cookies(response)
#     return response, 200
#
#
# # Обновление токена доступа
# @api.route("/refresh", methods=["GET"])
# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()
#     access_token = create_access_token(identity=identity)
#
#     response = jsonify({'msg': 'Refresh token is success', 'access_token': access_token})
#     set_access_cookies(response, access_token)
#     return response, 200
#
#

