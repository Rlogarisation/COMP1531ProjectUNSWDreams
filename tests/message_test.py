import pytest
from src.data_file import data
from src.error import InputError, AccessError
from src.auth import auth_register_v1, auth_login_v1, get_user_by_token
from src.channels import channels_create_v1
from src.other import clear_v1
from src.message import message_send_v2
#############################################################################
#                                                                           #
#                        Test for message_send_v2                           #
#                                                                           #
#############################################################################
"""
test_message_send_v2():

Author: Shaozhen Yan

Background:
Send a message from authorised_user to the channel specified by channel_id. Note: Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel.

Parameters: (token, channel_id, message)
Return Type: { message_id }
HTTP Method: POST

InputError:
    - (Added) Invalid token.
    - Message is more than 1000 characters
AccessError:
    - (Added) Invalid channel_id
    - the authorised user has not joined the channel they are trying to post to

"""


def test_message_send_invalid_token_v1():

    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")['token']
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    with pytest.raises(InputError):
        message_send_v2('invlaid_token', channel_0_id, 'it works!')



def test_message_send_long_message_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")['token']
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    long_message = "m" * 1001

    with pytest.raises(InputError):
        message_send_v2(token_0, channel_0_id, long_message)

def test_message_send_invalid_channel_id_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")['token']
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']

    assert message_id == message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']
    
    with pytest.raises(AccessError):
        message_send_v2(token_0, 'invalid channel_id', 'it not works')

def test_message_send_not_join_v1():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")['token']
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']

    token_1 = auth_register_v1("test_email1@email.com", "password", "First1", "Last1")['token']
    invalid_sender = auth_login_v1("test_email1@email.com", "password")
    
    with pytest.raises(AccessError):
        message_send_v2(token_1, channel_0_id, "You can't send msg")

def test_message_send_short_characters():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First", "Last")['token']
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    long_message = "m" * 1000
