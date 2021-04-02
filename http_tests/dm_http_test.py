import pytest
import requests
import json
from src import config
"""
http server tests of dm.py
Auther: Zheng Luo
"""

@pytest.fixture
def parameters0():
    parameters0 = {
        "email": "ZhengRogerLuo@gmail.com",
        "password": "TrimesterIsTheBest2021!",
        "name_first": "Zheng",
        "name_last": "Luo"
    }
    return parameters0

@pytest.fixture
def parameters1():
    parameters1 = {
        "email": "z5206267@gmail.com",
        "password": "IHateSemester2019!",
        "name_first": "Roger",
        "name_last": "Luo"
    }
    return parameters1


#############################################################################
#                                                                           #
#                     Http Test for dm_create_v1 Error                      #
#                                                                           #
#############################################################################

def test_dm_create_v1_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    token1 = json.loads(user1.text).get('token')
    u_id0 = json.loads(user0.text).get('auth_user_id')
    u_id1 = json.loads(user1.text).get('auth_user_id')
    incorrect_input = {
        'token': token0,
        'u_id_list': [1]
    }
    status = requests.post(config.url + 'dm/create/v1', json=incorrect_input).status_code
    assert status == 400



#############################################################################
#                                                                           #
#                     Http Test for dm_invite_v1 Error                      #
#                                                                           #
#############################################################################

def test_dm_invite_v1_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    token1 = json.loads(user1.text).get('token')
    input0 = {
        'token': token0,
        'u_id_list':[1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token0,
        'dm_id': dm_id,
        'u_id': '12'
    }
    status = requests.post(config.url + 'dm/invite/v1', json=incorrect_input).status_code
    assert status == 400
