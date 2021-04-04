import pytest
import requests
import json
from src import config

"""
http server tests of message.py
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


@pytest.fixture
def parameters1():
    parameters = {
        "email": "haha1@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    return parameters


@pytest.fixture
def parameters2():
    parameters = {
        "email": "haha2@gmail.com",
        "password": "123iwuiused",
        "name_first": "Lan",
        "name_last": "Lin"
    }
    return parameters

#############################################################################
#                                                                           #
#                       http test for message_send Error                    #
#                                                                           #
#############################################################################


def test_message_send_invalid_length_http(parameters):
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(user.text).get('token')
    json_input1 = {"token": token, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + 'channels/create/v2', json=json_input1)
    channel_id = json.loads(channel.text).get('channel_id')

    msg = "a" * 1005
    json_input2 = {"token": token, "channel_id": channel_id, "message": msg}
    status = requests.post(config.url + 'message/send/v2', json=json_input2).status_code
    assert status == 400


def test_message_send_not_join_http(parameters, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    token1 = json.loads(user1.text).get('token')

    json_input1 = {"token": token0, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + 'channels/create/v2', json=json_input1)
    channel_id = json.loads(channel.text).get('channel_id')

    json_input2 = {"token": token1, "channel_id": channel_id, "message": "haha"}
    status = requests.post(config.url + 'message/send/v2', json=json_input2).status_code
    assert status == 403
#############################################################################
#                                                                           #
#                       http test for message_edit Error                    #
#                                                                           #
#############################################################################


def test_message_edit_deleted_msg_http(parameters):
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(user.text).get('token')
    json_input1 = {"token": token, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + 'channels/create/v2', json=json_input1)
    channel_id = json.loads(channel.text).get('channel_id')

    json_input2 = {"token": token, "channel_id": channel_id, "message": "first"}
    msg_id = requests.post(config.url + 'message/send/v2', json=json_input2)
    message_id = json.loads(msg_id.text).get('message_id')

    requests.delete(config.url + 'message/remove/v1', json={"token": token, "message_id": message_id})
    json_input3 = {"token": token, "message_id": message_id, "message": "second"}
    status = requests.put(config.url + 'message/edit/v2', json=json_input3).status_code
    assert status == 400


def test_message_edit_accessError(parameters, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    token1 = json.loads(user1.text).get('token')

    json_input1 = {"token": token0, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + 'channels/create/v2', json=json_input1)
    channel_id = json.loads(channel.text).get('channel_id')
    st = requests.post(config.url + 'channel/join/v2', json={"token": token1, "channel_id": channel_id}).status_code
    assert st == 200

    json_input2 = {"token": token0, "channel_id": channel_id, "message": "haha"}
    msg_id = requests.post(config.url + 'message/send/v2', json=json_input2)
    message_id = json.loads(msg_id.text).get('message_id')

    json_input3 = {"token": token1, "message_id": message_id, "message": "heihei"}
    status = requests.put(config.url + 'message/edit/v2', json=json_input3).status_code
    assert status == 403
#############################################################################
#                                                                           #
#                       http test for message_remove Error                    #
#                                                                           #
#############################################################################


def test_message_remove_invalid_msg_id(parameters):
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json=parameters)
    token = json.loads(user.text).get('token')
    json_input1 = {"token": token, "name": "channel0", "is_public": True}
    requests.post(config.url + 'channels/create/v2', json=json_input1)

    json_input2 = {"token": token, "message_id": "haha"}
    status = requests.delete(config.url + 'message/remove/v1', json=json_input2).status_code
    assert status == 400


def test_message_remove_accessError(parameters, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    token1 = json.loads(user1.text).get('token')

    json_input1 = {"token": token0, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + 'channels/create/v2', json=json_input1)
    channel_id = json.loads(channel.text).get('channel_id')
    requests.post(config.url + 'channel/join/v2', json={"token": token1, "channel_id": channel_id})

    json_input2 = {"token": token0, "channel_id": channel_id, "message": "haha"}
    requests.post(config.url + 'message/send/v2', json=json_input2)
    msg_id = requests.post(config.url + 'message/send/v2', json=json_input2)
    message_id = json.loads(msg_id.text).get('message_id')

    json_input3 = {"token": token1, "message_id": message_id}
    status = requests.delete(config.url + 'message/remove/v1', json=json_input3).status_code
    assert status == 403
#############################################################################
#                                                                           #
#                       http test for message_share Error                    #
#                                                                           #
#############################################################################


def test_message_share_not_join_http(parameters, parameters1):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    token1 = json.loads(user1.text).get('token')

    json_input1 = {"token": token0, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + 'channels/create/v2', json=json_input1)
    channel_id = json.loads(channel.text).get('channel_id')

    json_input2 = {"token": token0, "channel_id": channel_id, "message": "haha"}
    requests.post(config.url + 'message/send/v2', json=json_input2)
    msg_id = requests.post(config.url + 'message/send/v2', json=json_input2)
    og_message_id = json.loads(msg_id.text).get('message_id')
    json_input3 = {
        "token": token1,
        "og_message_id": og_message_id,
        "message": "good",
        "channel_id": channel_id,
        "dm_id": -1
    }
    status = requests.post(config.url + 'message/share/v1', json=json_input3).status_code
    assert status == 403
#############################################################################
#                                                                           #
#                       http test for message_senddm Error                    #
#                                                                           #
#############################################################################


def test_message_senddm_invalid_length_http(parameters):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters)
    uid1 = json.loads(user1.text).get('auth_user_id')
    json_input1 = {"token": token0, "u_ids": [uid1]}
    dm = requests.post(config.url + 'dm/create/v1', json=json_input1)
    dm_id = json.loads(dm.text).get('dm_id')

    msg = "a" * 1005
    json_input2 = {"token": token0, "dm_id": dm_id, "message": msg}
    status = requests.post(config.url + 'message/senddm/v1', json=json_input2).status_code
    assert status == 400


def test_message_senddm_not_join_http(parameters, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    uid1 = json.loads(user1.text).get('auth_user_id')
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    token2 = json.loads(user2.text).get('token')

    json_input1 = {"token": token0, "u_ids": [uid1]}
    dm = requests.post(config.url + 'dm/create/v1', json=json_input1)
    dm_id = json.loads(dm.text).get('dm_id')

    json_input2 = {"token": token2, "dm_id": dm_id, "message": "haha"}
    status = requests.post(config.url + 'message/senddm/v1', json=json_input2).status_code
    assert status == 403
#############################################################################
#                                                                           #
#                       http test for message successfully                  #
#                                                                           #
#############################################################################


"""
successful tests for message_send, message_senddm, message_edit,
message_remove, message_share, channel_messages, dm_messages
"""


def test_message_valid_http(parameters, parameters1, parameters2):
    requests.delete(config.url + 'clear/v1')
    user0 = requests.post(config.url + 'auth/register/v2', json=parameters)
    token0 = json.loads(user0.text).get('token')
    user1 = requests.post(config.url + 'auth/register/v2', json=parameters1)
    uid1 = json.loads(user1.text).get('auth_user_id')
    user2 = requests.post(config.url + 'auth/register/v2', json=parameters2)
    token2 = json.loads(user2.text).get('token')

    # create a dm, users in dm are user0, 1
    json_input1 = {"token": token0, "u_ids": [uid1]}
    dm = requests.post(config.url + 'dm/create/v1', json=json_input1)
    dm_id = json.loads(dm.text).get('dm_id')

    # create a channel by user2
    json_input2 = {"token": token2, "name": "channel0", "is_public": True}
    channel = requests.post(config.url + 'channels/create/v2', json=json_input2)
    channel_id = json.loads(channel.text).get('channel_id')

    # send a message to the dm
    json_input3 = {"token": token0, "dm_id": dm_id, "message": "haha0"}
    requests.post(config.url + 'message/senddm/v1', json=json_input3)

    # check the message in the dm
    dm_msg = requests.get(config.url + 'dm/messages/v1?token=' + token0 + '&dm_id=' + str(dm_id) + '&start=0')
    dm_msg = json.loads(dm_msg.text).get('messages')[0]
    assert dm_msg['message'] == "haha0"
    message_id = dm_msg['message_id']

    # edit the message in the dm
    # check the edited message in the dm
    json_input7 = {"token": token0, "message_id": message_id, "message": "haha1"}
    requests.put(config.url + 'message/edit/v2', json=json_input7)
    dm_msg = requests.get(config.url + 'dm/messages/v1?token=' + token0 + '&dm_id=' + str(dm_id) + '&start=0')
    dm_msg = json.loads(dm_msg.text).get('messages')[0]
    assert dm_msg['message'] == "haha1"

    # remove the message in the dm
    json_input8 = {"token": token0, "message_id": message_id}
    requests.delete(config.url + 'message/remove/v1', json=json_input8)
    # check that the message has been removed
    dm_msg = requests.get(config.url + 'dm/messages/v1?token=' + token0 + '&dm_id=' + str(dm_id) + '&start=0')
    dm_msg = json.loads(dm_msg.text).get('messages')
    assert len(dm_msg) == 0

    # send 60 messages to the channel
    for _i in range(60):
        json_input4 = {"token": token2, "channel_id": channel_id, "message": f"good{_i}"}
        requests.post(config.url + 'message/send/v2', json=json_input4)

    # check if the message are sent successfully
    channel_msg = requests.get(config.url + 'channel/messages/v2?token=' + token2 + '&channel_id=' +
                               str(channel_id) + '&start=5')
    channel_msg = json.loads(channel_msg.text)
    message_list = channel_msg.get('messages')
    start = channel_msg.get('start')
    end = channel_msg.get('end')
    assert message_list[0]['message'] == "good54"
    assert len(message_list) == 50
    assert start == 5
    assert end == 55

    # share the first message in the channel to the dm
    json_input9 = {
        "token": token0,
        "og_message_id": 1,
        "message": "this is comment",
        "channel_id": -1,
        "dm_id": 0
    }
    assert requests.post(config.url + 'message/share/v1', json=json_input9).status_code == 200
    # check if the message has been shared successfully
    dm_msg = requests.get(config.url + 'dm/messages/v1?token=' + token0 + '&dm_id=' + str(dm_id) + '&start=0')
    dm_msg = json.loads(dm_msg.text).get('messages')[0]['message']
    correct = 'this is comment' \
              '"""' \
              'good0' \
              '"""'
    assert dm_msg == correct
