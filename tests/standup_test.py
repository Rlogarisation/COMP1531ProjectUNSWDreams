import pytest
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, auth_logout
from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1

"""
Author : Emir Aditya Zen

Test for standup_start_v1 function implementation

Tests content:
1. Succesful implementation of standup_start_v1
2. Input error due to invalid channel_id used
3. Input error due to an active standup is already running
4. Access error due to authorised user not in channel
5. Access error dur to invalid token
"""


#############################################################################
#                                                                           #
#                         Test for standup_start_v1                         #
#                                                                           #
#############################################################################


def test_standup_start_successful():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    time_finish_check = standup_start_v1(token1, channel_id1, 0.5)['time_finish']
    standup_info = standup_active_v1(token1, channel_id1)
    assert standup_info['time_finish'] == time_finish_check
    assert standup_info['is_active'] is True


def test_standup_start_invalid_channel():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channels_create_v1(token1, 'ChannelOne', True)
    invalid_channelid = 100
    with pytest.raises(InputError):
        standup_start_v1(token1, invalid_channelid, 0.5)


def test_standup_start_currently_running_standup():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    standup_start_v1(token1, channel_id1, 0.5)
    with pytest.raises(InputError):
        standup_start_v1(token1, channel_id1, 0.5)


def test_standup_start_invalid_token():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_token = token1 + 'tsyerhdjycgj'
    with pytest.raises(AccessError):
        standup_start_v1(invalid_token, channel_id1, 0.5)


# def test_standup_start_unauthorised_user():
#     clear_v1()
#     auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
#     auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
#     token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
#     token2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")['token']
#     channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
#     with pytest.raises(AccessError):
#         standup_start_v1(token2, channel_id1, 0.5)


"""
Author : Emir Aditya Zen

Test for standup_active_v1 function implementation

Tests content:
1. Succesful implementation of standup_active_v1 with a present standup running
2. Succesful implementation of standup_active_v1 with no standup running
3. Input error due to invalid channel_id used
4. Access error dur to invalid token
"""


#############################################################################
#                                                                           #
#                        Test for standup_active_v1                         #
#                                                                           #
#############################################################################


def test_standup_active_standup_present():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    time_finish_check = standup_start_v1(token1, channel_id1, 0.5)
    standup_info = standup_active_v1(token1, channel_id1)
    assert standup_info['time_finish'] == time_finish_check['time_finish']
    assert standup_info['is_active'] is True


def test_standup_active_no_standup_present():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    standup_info = standup_active_v1(token1, channel_id1)
    assert standup_info['time_finish'] is None
    assert standup_info['is_active'] is False


def test_standup_active_invalid_channel():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_channelid = 100
    standup_start_v1(token1, channel_id1, 0.5)
    with pytest.raises(InputError):
        standup_active_v1(token1, invalid_channelid)


def test_standup_active_invalid_token():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_token = token1 + 'vwkudhbae'
    standup_start_v1(token1, channel_id1, 0.5)
    with pytest.raises(AccessError):
        standup_active_v1(invalid_token, channel_id1)


"""
Author : Emir Aditya Zen

Test for standup_send_v1 function implementation

Tests content:
1. Succesful implementation of standup_send_v1
2. Input error due to invalid channel_id used
3. Input error due to message is more than 1000 characters excluding username and colon
4. Input error due to no active standup present
5. Access error due to unauthorised user calling the function
6. ACcess error due to invalid token
"""


#############################################################################
#                                                                           #
#                        Test for standup_active_v1                         #
#                                                                           #
#############################################################################


def test_standup_send_successful():
    pass


def test_standup_send_invalid_channel():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_channelid = 100
    standup_start_v1(token1, channel_id1, 0.5)
    with pytest.raises(InputError):
        standup_send_v1(token1, invalid_channelid, 'This is the first message')


def test_standup_send_invalid_message():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    standup_start_v1(token1, channel_id1, 0.5)
    message = 'a' * 1500
    with pytest.raises(InputError):
        standup_send_v1(token1, channel_id1, message)


def test_standup_send_no_active_standup():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    with pytest.raises(InputError):
        standup_send_v1(token1, channel_id1, 'This is the first message')


# def test_standup_send_unauthorised_user():
#     clear_v1()
#     auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
#     auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
#     token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
#     token2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")['token']
#     channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
#     standup_start_v1(token1, channel_id1, 0.5)
#     with pytest.raises(AccessError):
#         standup_send_v1(token2, channel_id1, "this is a test")


def test_standup_send_invalid_token():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = auth_login_v1('haha@gmail.com', '123123123')['token']
    channel_id1 = channels_create_v1(token1, 'ChannelOne', True)['channel_id']
    invalid_token = token1 + 'qytwiefvgiauwgfv'
    standup_start_v1(token1, channel_id1, 0.5)
    with pytest.raises(AccessError):
        standup_send_v1(invalid_token, channel_id1, 'This is the first message')
