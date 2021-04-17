import pytest
import requests
import json
from time import sleep
from requests.models import ContentDecodingError
from src import config
from tests.auth_test import get_email_content, parser_reset_code
"""
http server tests of auth.py
Auther: Lan Lin
"""


@pytest.fixture
def parameters():
    parameters = {
        "email": "haha@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    return parameters
#############################################################################
#                                                                           #
#                       http test for auth_register Error                   #
#                                                                           #
#############################################################################


def test_auth_register_invalid_email_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "123.com",
        "password": "12345ufd",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400
    requests.delete(config.url + "clear/v1")


def test_auth_register_duplicate_email_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "123.com",
        "password": "12345ufd",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    requests.post(config.url + 'auth/register/v2', json=parameters)
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400
    requests.delete(config.url + "clear/v1")


def test_auth_register_pwd_length_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "haha@gmail.com",
        "password": "123",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400
    requests.delete(config.url + "clear/v1")


def test_auth_register_firstName_length_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "haha@gmail.com",
        "password": "123iwuiused",
        "name_first": "",
        "name_last": "Lin"
    }
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400
    requests.delete(config.url + "clear/v1")


def test_auth_register_lastName_length_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "haha@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": ""
    }
    status = requests.post(config.url + 'auth/register/v2', json=parameters).status_code
    assert status == 400
    requests.delete(config.url + "clear/v1")
#############################################################################
#                                                                           #
#                       http test for auth_login Error                   #
#                                                                           #
#############################################################################


def test_auth_login_invalid_email_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "123.com",
        "password": "12345ufd",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    status = requests.post(config.url + 'auth/login/v2', json=parameters).status_code
    assert status == 400
    requests.delete(config.url + "clear/v1")


def test_auth_login_not_registered_email_http():
    requests.delete(config.url + 'clear/v1')
    parameters = {
        "email": "haha@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    requests.post(config.url + 'auth/register/v2', json=parameters)
    parameters2 = {
        "email": "haha1@gmail.com",
        "password": "123iwuiused"
    }
    status = requests.post(config.url + 'auth/login/v2', json=parameters2).status_code
    assert status == 400
    requests.delete(config.url + "clear/v1")


def test_auth_login_wrong_password_http(parameters):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=parameters)
    parameters2 = {
        "email": "haha@gmail.com",
        "password": "123iwuiusepp"
    }
    status = requests.post(config.url + 'auth/login/v2', json=parameters2).status_code
    assert status == 400
    requests.delete(config.url + "clear/v1")
#############################################################################
#                                                                           #
#                       http test for auth_logout Error                     #
#                                                                           #
#############################################################################


def test_auth_logout_invalid_token_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(resp.text).get('token')
    invalid_token = f"{token}123"
    resp = requests.post(config.url + 'auth/logout/v1', json={"token": invalid_token})
    assert json.loads(resp.text).get('is_success') is False
    requests.delete(config.url + "clear/v1")
#############################################################################
#                                                                           #
#          http test for auth_register, auth_login, auth_logout             #
#                                                                           #
#############################################################################


"""
http tests for auth_register, auth_login, auth_logout successfully
to test logout, the test calls auth_register and auth_login,
which tests the three functions together
"""


def test_auth_logout_successfully_http(parameters):
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json=parameters)
    parameters2 = {
        "email": "haha@gmail.com",
        "password": "123iwuiused"
    }
    resp2 = requests.post(config.url + 'auth/login/v2', json=parameters2)
    auth_user_id0 = json.loads(resp.text).get('auth_user_id')
    auth_user_id1 = json.loads(resp2.text).get('auth_user_id')
    token0 = json.loads(resp.text).get('token')
    token1 = json.loads(resp2.text).get('token')
    assert auth_user_id0 == 0
    assert auth_user_id1 == 0
    resp_logout0 = requests.post(config.url + 'auth/logout/v1', json={"token": token0})
    resp_logout1 = requests.post(config.url + 'auth/logout/v1', json={"token": token1})
    assert json.loads(resp_logout0.text).get('is_success') is True
    assert json.loads(resp_logout1.text).get('is_success') is True
    requests.delete(config.url + "clear/v1")


#############################################################################
#                                                                           #
#   Test for auth_passwordreset_request_v1 and auth_passwordreset_reset_v1  #
#                                                                           #
#############################################################################

def test_auth_passwordreset_successful():
    requests.delete(config.url + "clear/v1")

    input1 = {"email": 'styuannj@163.com', "password": '123123123', "name_first": 'Peter', "name_last": 'White'}
    user_1 = requests.post(config.url + 'auth/register/v2', json=input1)
    id_check_1 = json.loads(user_1.text).get("auth_user_id")

    code_sent = requests.post(config.url + "auth/passwordreset/request/v1", json={"email": 'styuannj@163.com'})
    reset_code_1 = json.loads(code_sent.text).get('reset_code')

    sleep(2)
    msg = get_email_content("styuannj@163.com", "UXRVCTIAEQZVVGAG", "pop.163.com")

    reset_code_2 = parser_reset_code(msg)

    assert reset_code_1 == reset_code_2

    requests.post(config.url + 'auth/passwordreset/reset/v1', json={"reset_code": reset_code_2, "new_password": 'TheNewPassword'})

    user_2 = requests.post(config.url + 'auth/register/v2', json={"email": 'styuannj@163.com', "password": 'TheNewPassword'})
    id_check_2 = json.loads(user_2.text).get("auth_user_id")

    assert id_check_1 == id_check_2

    pass

    requests.delete(config.url + "clear/v1")


def test_auth_passwordrequest_invalid_email():
    requests.delete(config.url + "clear/v1")

    input1 = {"email": 'cblinker17@gmail.com', "password": '123123123', "name_first": 'Peter', "name_last": 'White'}
    user_1 = requests.post(config.url + 'auth/register/v2', json=input1)

    status1 = requests.post(config.url + "auth/passwordreset/request/v1", json={"email": 'cblinker@gmail.com'}).status_code

    assert status1 == 400
    pass

    requests.delete(config.url + "clear/v1")


def test_auth_passwordreset_reset_invalid_password():
    requests.delete(config.url + "clear/v1")

    input1 = {"email": 'cblinker17@gmail.com', "password": '123123123', "name_first": 'Peter', "name_last": 'White'}
    requests.post(config.url + 'auth/register/v2', json=input1)

    code_sent = requests.post(config.url + "auth/passwordreset/request/v1", json={"email": 'cblinker17@gmail.com'})
    reset_code_1 = json.loads(code_sent.text).get('reset_code')

    invalid_password = '123'
    stauts1 = requests.post(config.url + 'auth/passwordreset/reset/v1', json={"reset_code": reset_code_1, "new_password": invalid_password}).status_code

    assert stauts1 == 400

    pass

    requests.delete(config.url + "clear/v1")


def test_auth_passwordreset_reset_invalid_reset_code():
    requests.delete(config.url + "clear/v1")

    input1 = {"email": 'cblinker17@gmail.com', "password": '123123123', "name_first": 'Peter', "name_last": 'White'}
    requests.post(config.url + 'auth/register/v2', json=input1)

    code_sent = requests.post(config.url + "auth/passwordreset/request/v1", json={"email": 'cblinker17@gmail.com'})
    reset_code_1 = json.loads(code_sent.text).get('reset_code')

    invalid_reset_code = reset_code_1 + 123

    stauts1 = requests.post(config.url + 'auth/passwordreset/reset/v1', json={"reset_code": invalid_reset_code, "new_password": 'TheNewPassword'}).status_code

    assert stauts1 == 400
    pass

    requests.delete(config.url + "clear/v1")
