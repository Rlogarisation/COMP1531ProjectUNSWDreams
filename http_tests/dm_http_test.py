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
        "email": "z5206267@ad.unsw.edu.au",
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

def test_dm_create_v1_http():
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    token1 = json.loads(user1.text).get('token')
    incorrect_input = {
        'token': token0,
        'u_id_list': [4, 5]
    }
    status = requests.post(config.url + 'dm/create/v1', json=incorrect_input).status_code
    assert status == 400