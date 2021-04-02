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

@pytest.fixture
def parameters2():
    parameters2 = {
        "email": "hahahaah2@gmail.com",
        "password": "IHateSemester2020!",
        "name_first": "James",
        "name_last": "Brown"
    }
    return parameters2



#############################################################################
#                                                                           #
#                     Http Test for dm_create_v1 Error                      #
#                                                                           #
#############################################################################

# Invalid input invitee
def test_dm_create_v1_nonexist_invitee_http(parameters0):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    incorrect_input = {
        'token': token0,
        'u_ids': [5]
    }
    status = requests.post(config.url + 'dm/create/v1', json=incorrect_input).status_code
    assert status == 400



#############################################################################
#                                                                           #
#                     Http Test for dm_invite_v1 Error                      #
#                                                                           #
#############################################################################

# Invaild input u_id
def test_dm_invite_v1_invaild_uid_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids':[u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token0,
        'dm_id': dm_id,
        'u_ids': '12'
    }
    status = requests.post(config.url + 'dm/invite/v1', json=incorrect_input).status_code
    assert status == 400

# Invaild input dm_id
def test_dm_invite_v1_invaild_dm_id_http(parameters0, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    u_id_2 = json.loads(user2.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids':[u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token0,
        'dm_id': 'incorrect_dm_id',
        'u_ids': u_id_2
    }
    status = requests.post(config.url + 'dm/invite/v1', json=incorrect_input).status_code
    assert status == 400

# Access error already a user
def test_dm_invite_v1_already_user_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    # Create(register) two users: user0 and user1.
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids':[u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token0,
        'dm_id': dm_id,
        'u_ids': u_id_1
    }
    status = requests.post(config.url + 'dm/invite/v1', json=incorrect_input).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                     Http Test for dm_remove_v1 Error                      #
#                                                                           #
#############################################################################
'''
Parameters: (token, dm_id)
Return Type: {}
HTTP Method: DELETE
'''
# Invaild input dm_id
def test_dm_remove_v1_invaild_dm_id_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids':[u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    incorrect_input = {
        'token': token0,
        'dm_id': 'incorrect_value'
    }
    status = requests.delete(config.url + 'dm/remove/v1', json=incorrect_input).status_code
    assert status == 400


# Case: Not the original creator to remove the dm.
def test_dm_remove_v1_incorrect_token_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    token1 = json.loads(user1.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids':[u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token1,
        'dm_id': dm_id
    }
    status = requests.delete(config.url + 'dm/remove/v1', json=incorrect_input).status_code
    assert status == 403

#############################################################################
#                                                                           #
#                     Http Test for dm_leave_v1 Error                      #
#                                                                           #
#############################################################################
"""
Author: Zheng Luo

dm/leave/v1

Background:
Given a DM ID, the user is removed as a member of this DM

Parameters: (token, dm_id)
Return Type: {}
HTTP Method: POST

InputError when any of:
    dm_id is not a valid DM

AccessError when
    Authorised user is not a member of DM with dm_id

"""

# Invalid dm_id => inputError => 400
def test_dm_leave_v1_invaild_dm_id_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids':[u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    incorrect_input = {
        'token': token0,
        'dm_id': "invalid_dm_id"
    }
    status = requests.post(config.url + 'dm/leave/v1', json=incorrect_input).status_code
    assert status == 400

# The test user is not in the dm yet => accessError => 403
# user0 invite user1
# error when user2 want to leave dm_id 0
def test_dm_leave_v1_invaild_dm_id_http(parameters0, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    token2 = json.loads(user2.text).get('token')
    input0 = {
        'token': token0,
        'u_ids':[u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token2,
        'dm_id': dm_id
    }
    status = requests.post(config.url + 'dm/leave/v1', json=incorrect_input).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                     Http Test for dm_detail_v1 Error                      #
#                                                                           #
#############################################################################
"""
Author: Zheng Luo

dm/details/v1

Background:
Users that are part of this direct message can view basic information about the DM

Parameters: (token, dm_id)
Return Type: { name, members }
HTTP Method: GET

InputError when any of:
    DM ID is not a valid DM

AccessError when
    Authorised user is not a member of this DM with dm_id
"""
# dm_id is not a valid dm
def test_dm_detail_v1_invaild_dm_id_http(parameters0, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids':[u_id_1]
    }
    incorrect_input = {
        'token': token0,
        'dm_id': "invalid_dm_id"
    }
    status = requests.get(config.url + 'dm/detail/v1', json=incorrect_input).status_code
    assert status == 400

# Authorised user is not a member of this DM with dm_id
def test_dm_detail_v1_unauth_user_http(parameters0, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters0)
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    # Obtain tokens based on registered users.
    token0 = json.loads(user0.text).get('token')
    token2 = json.loads(user2.text).get('token')

    u_id_1 = json.loads(user1.text).get('auth_user_id')
    input0 = {
        'token': token0,
        'u_ids':[u_id_1]
    }
    dm_info = requests.post(config.url + 'dm/create/v1', json=input0)
    dm_id = json.loads(dm_info.text).get('dm_id')
    incorrect_input = {
        'token': token2,
        'dm_id': dm_id
    }
    status = requests.get(config.url + 'dm/detail/v1', json=incorrect_input).status_code
    assert status == 403


#############################################################################
#                                                                           #
#                     Http Test for dm_list_v1 Error                      #
#                                                                           #
#############################################################################
"""
dm_list_v1():

Returns the list of DMs that the user is a member of.

Parameters:(token)
Return Type:{ dms }
HTTP Method: GET

TEST CASES:
	N/A
"""

