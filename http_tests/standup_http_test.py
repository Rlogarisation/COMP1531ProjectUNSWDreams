import pytest
import requests
import json
from src import config
"""
http server tests of standup.py
Author: Emir Aditya Zen
"""

@pytest.fixture
def user1():
    user1 = {
        "email": "haha@gmail.com",
        "password": "123123123",
        "name_first": "Peter",
        "name_last": "White"
    }
    return user1

@pytest.fixture
def user2():
    user2 = {
        "email": "test@testexample.com",
        "password": "wp01^#$dp1o23",
        "name_first": "Tom",
        "name_last": "Green"
    }
    return user2

message = "This is the message used for standup send"
invalid_message = "This is the invalid message for standup send" + "a"*1500

#############################################################################
#                                                                           #
#                       http test for standup_start Error                   #
#                                                                           #
#############################################################################

def test_standup_start_invalid_channel_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    invalid_channelid = channel_id + 123
    output = requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":invalid_channelid,"length":50}).status_code
    assert output == 400

def test_standup_start_currently_running_standup_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":channel_id,"length":50})
    output = requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":channel_id,"length":50}).status_code
    assert output == 400

def test_standup_start_unauthorised_user(user1, user2):
    requests.delete(config.url + 'clear/v1')
    user1_register = requests.post(config.url + 'auth/register/v2', json=user1)
    user2_register = requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'standup/start/v1', json={"token":token2,"channel_id":channel_id,"length":50}).status_code
    assert output == 403

def test_standup_start_invalid_token(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    invalid_token = f"{token1}123"
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'standup/start/v1', json={"token":invalid_token,"channel_id":channel_id,"length":50}).status_code
    assert output == 403

#############################################################################
#                                                                           #
#                      http test for standup_active Error                   #
#                                                                           #
#############################################################################

def test_standup_active_invalid_channel_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    invalid_channelid = channel_id + 123
    requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":channel_id,"length":50})
    output = requests.get(config.url + 'standup/active/v1' + f'?token={token1}&channel_id={invalid_channelid}').status_code
    assert output == 400

def test_standup_active_invalid_token_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    invalid_token = channel_id + 123
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":channel_id,"length":50})
    output = requests.get(config.url + 'standup/active/v1' + f'?token={invalid_token}&channel_id={channel_id}').status_code
    assert output == 403

#############################################################################
#                                                                           #
#                      http test for standup_send Error                     #
#                                                                           #
#############################################################################

def test_standup_send_invalid_channel_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    invalid_channelid = channel_id + 123
    requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":channel_id,"length":50})
    output = requests.post(config.url + 'standup/send/v1', json={"token":token1,"channel_id":invalid_channelid,"message":message}).status_code
    assert output == 400

def test_standup_send_invalid_message_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":channel_id,"length":50})
    output = requests.post(config.url + 'standup/send/v1', json={"token":token1,"channel_id":channel_id,"message":invalid_message}).status_code
    assert output == 400

def test_standup_send_no_active_standup_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    output = requests.post(config.url + 'standup/send/v1', json={"token":token1,"channel_id":channel_id,"message":message}).status_code
    assert output == 400

def test_standup_send_unauthorised_user_http(user1, user2):
    requests.delete(config.url + 'clear/v1')
    user1_register = requests.post(config.url + 'auth/register/v2', json=user1)
    user2_register = requests.post(config.url + 'auth/register/v2', json=user2)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    user2_login = requests.post(config.url + 'auth/login/v2', json=user2)
    token1 = json.loads(user1_login.text).get('token')
    token2 = json.loads(user2_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":channel_id,"length":50})
    output = requests.post(config.url + 'standup/send/v1', json={"token":token2,"channel_id":channel_id,"message":message}).status_code
    assert output == 403

def test_standup_send_invalid_token_http(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    invalid_token = f"{token1}123"
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":channel_id,"length":50})
    output = requests.post(config.url + 'standup/send/v1', json={"token":invalid_token,"channel_id":channel_id,"message":message}).status_code
    assert output == 403
    
#############################################################################
#                                                                           #
#                      http test for succesful cases                        #
#                                                                           #
#############################################################################

def test_standup_success_standup(user1):
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json=user1)
    user1_login = requests.post(config.url + 'auth/login/v2', json=user1)
    token1 = json.loads(user1_login.text).get('token')
    channel = requests.post(config.url + 'channels/create/v2', json={"token":token1,"name":"channelone","is_public":True})
    channel_id = json.loads(channel.text).get('channel_id')

    # Test valid standup active implementation when no standup occurs
    standup_active_test1 = requests.get(config.url + 'standup/active/v1' + f'?token={token1}&channel_id={channel_id}')
    assert standup_active_test1.status_code == 200
    assert json.loads(standup_active_test1.text).get('is_active') == False
    assert json.loads(standup_active_test1.text).get('time_finish') == None

    # Test valid standup start implementation
    standup_start_test = requests.post(config.url + 'standup/start/v1', json={"token":token1,"channel_id":channel_id,"length":50})
    assert standup_start_test.status_code == 200
    finish_time = json.loads(standup_start_test.text).get('time_finish')

    # Test valid standup active implementation when there is standup occuring
    standup_active_test1 = requests.get(config.url + 'standup/active/v1' + f'?token={token1}&channel_id={channel_id}')
    assert standup_active_test2.status_code == 200
    assert json.loads(standup_active_test2.text).get('is_active') == True
    assert json.loads(standup_active_test2.text).get('time_finish') == finish_time

    # Test valid standup send implementation
    standup_send_test = requests.post(config.url + 'standup/send/v1', json={"token":invalid_token,"channel_id":channel_id,"message":message})
    assert standup_send_test.status_code == 200
