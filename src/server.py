import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.data_file import data, dump_data
from src.auth import auth_register_v1, auth_login_v1, auth_logout
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1, \
    users_all, admin_user_remove, admin_userpermission_change


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })
#############################################################################
#                                                                           #
#                           Server for auth.py                              #
#                                                                           #
#############################################################################


@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_v2():
    info = request.get_json()
    email = info['email']
    password = info['password']
    name_first = info['name_first']
    name_last = info['name_last']
    result = auth_register_v1(email, password, name_first, name_last)
    dump_data(data)
    return dumps(result)


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_v2():
    info = request.get_json()
    result = auth_login_v1(info['email'], info['password'])
    dump_data(data)
    return dumps(result)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout_v1():
    info = request.get_json()
    result = auth_logout(info['token'])
    dump_data(data)
    return dumps(result)
#############################################################################
#                                                                           #
#                           Server for user.py                              #
#                                                                           #
#############################################################################




if __name__ == "__main__":
    APP.run(port=config.port)  # Do not edit this port
