from src.channel import channel_invite_v1, channel_messages_v1
import pytest
from src.data_file import data
from src.dm import dm_create_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.auth import auth_register_v2, auth_login_v1
from src.other import clear_v1
from src.message import message_send_v2, message_edit_v2, message_remove_v1, message_share_v1
#############################################################################
#                                                                           #
#                        Test for message_send_v2                           #
#                                                                           #
#############################################################################
"""

Author: Shaozhen Yan

Background:
Send a message from authorised_user to the channel specified by channel_id. 
Note: Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel.

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
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    with pytest.raises(InputError):
        message_send_v2('invlaid_token', channel_0_id, 'it works!')


def test_message_send_long_message_v1():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    long_message = "m" * 1001

    with pytest.raises(InputError):
        message_send_v2(token_0, channel_0_id, long_message)


def test_message_send_invalid_channel_id_v1():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']

    with pytest.raises(AccessError):
        message_send_v2(token_0, 'invalid channel_id', 'it not works')


def test_message_send_not_join_v1():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First0", "Last0")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']

    token_1 = auth_register_v2("test_email1@email.com", "password", "First1", "Last1")['token']
    invalid_sender = auth_login_v1("test_email1@email.com", "password")

    with pytest.raises(AccessError):
        message_send_v2(token_1, channel_0_id, "You can't send msg")


def test_message_send_same_message_id():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First0", "Last0")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    token_1 = auth_register_v2("test_email1@gmail.com", "password", "First1", "Last1")['token']
    auth_login_v1("test_email1@gmail.com", "password")
    # FixMe: 这边user1没有在channel_0里面，所以他不会有权限send message到channel， 我message.py里面在这边raise了accesserror
    message_1_id = message_send_v2(token_1, channel_0_id, 'Hope it works')['message_id']

    assert message_0_id != message_1_id


def test_message_send_valid_case():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    u_id = auth_login_v1("test_email0@gmail.com", "password")['auth_user_id']
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']
    all_messages = channel_messages_v1(token_0, channel_0_id, 0)

    assert all_messages['messages'][0].message == 'Hope it works'
    assert all_messages['messages'][0].message_id == message_0_id
    assert all_messages['messages'][0].u_id == u_id


#############################################################################
#                                                                           #
#                        Test for message_remove_v1                         #
#                                                                           #
#############################################################################
"""
Author: Shaozhen Yan

Background:
Given a message_id for a message, this message is removed from the channel/DM

Parameters: (token, message_id)
Return Type: {}
HTTP Method: DELETE

InputError:
    - (Added) Invalid token.
    - Message (based on ID) no longer exists
AccessError when none of the following are true:
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def test_message_remove_invalid_token():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    with pytest.raises(InputError):
        message_remove_v1('invlaid_token', message_0_id)


def test_message_remove_message_not_exist():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    

    with pytest.raises(InputError):
        message_remove_v1(token_0, -1)


def test_message_remove_not_owner_or_authorised_user():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First0", "Last0")['token']
    token_1 = auth_register_v2("test_email1@gmail.com", "password", "First1", "Last1")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")['auth_user_id']

    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    channel_invite_v1(token_0, channel_0_id, u_id_1)

    with pytest.raises(AccessError):
        message_remove_v1(token_1, message_0_id)


def test_message_remove_valid_case():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    assert message_remove_v1(token_0, message_0_id) == {}


#############################################################################
#                                                                           #
#                        Test for message_edit_v1                           #
#                                                                           #
#############################################################################
"""
Author: Shaozhen Yan

Background:
Given a message, update its text with new text. 
If the new message is an empty string, the message is deleted.

Parameters: (token, message_id, message)
Return Type: {}
HTTP Method: PUT

InputError:
    - (Added) Invalid token.
    - Length of message is over 1000 characters message_id refers to a deleted message
AccessError when none of the following are true:
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def test_message_edit_long_message():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    auth_login_v1("test_email0@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    long_message = "m" * 1000
    message_0_id = message_send_v2(token_0, channel_0_id, long_message)

    longer_message = "m" * 1001
    with pytest.raises(InputError):
        message_edit_v2(token_0, message_0_id, longer_message)


def test_message_edit_deleted_message():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")['auth_user_id']

    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']

    message_send_v2(token_0, channel_0_id, 'Hope it works')

    with pytest.raises(InputError):
        message_edit_v2(token_0, 'non_exist_message_id', 'It works')


def test_message_edit_not_owner_or_authorised_user():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First0", "Last0")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    token_1 = auth_register_v2("test_email1@gmail.com", "password", "First1", "Last1")['token']
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")['auth_user_id']

    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    channel_invite_v1(token_0, channel_0_id, u_id_1)

    with pytest.raises(AccessError):
        message_edit_v2(token_1, message_0_id, 'It works')


def test_message_edit_empty_message():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")['auth_user_id']

    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_0_id = message_send_v2(token_0, channel_0_id, '')['message_id']
    message_edit_v2(token_0, message_0_id, 'It works')
    all_messages = channel_messages_v1(token_0, channel_0_id, 0)

    assert all_messages['messages'][0]['message'] == 'It works'
    assert all_messages['messages'][0]['message_id'] == message_0_id
    assert all_messages['messages'][0]['u_id'] == u_id_0


def test_message_edit_valid_case():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First", "Last")['token']
    u_id = auth_login_v1("test_email0@gmail.com", "password")['auth_user_id']

    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    message_0_id = message_send_v2(token_0, channel_0_id, 'It works')

    message_edit_v2(token_0, message_0_id, 'It really works')
    all_messages = channel_messages_v1(token_0, channel_0_id, 0)

    assert all_messages['messages'][0]['message'] == 'It really works'
    assert all_messages['messages'][0]['message_id'] == message_0_id
    assert all_messages['messages'][0]['u_id'] == u_id


#############################################################################
#                                                                           #
#                        Test for message_share_v1                          #
#                                                                           #
#############################################################################
"""
Author: Shaozhen Yan

Background:
og_message_id is the original message. 
channel_id is the channel that the message is being shared to, and is -1 if it is being sent to a DM. 
dm_id is the DM that the message is being shared to, and is -1 if it is being sent to a channel. 
message is the optional message in addition to the shared message, and will be an empty string '' if no message is given

Parameters: (token, og_message_id, message, channel_id, dm_id)
Return Type: {shared_message_id}
HTTP Method: POST

InputError:
    - (Added) if neither channel_id nor dm_id is -1 or both are -1

AccessError: 
    - the authorised user has not joined the channel or DM they are trying to share the message to

"""


def test_message_share_not_joing_channel():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First0", "Last0")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    token_1 = auth_register_v2("test_email1@gmail.com", "password", "First1", "Last1")['token']
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")['auth_user_id']

    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    og_message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages['messages'][0].message

    with pytest.raises(AccessError):
        message_share_v1(token_1, og_message_0_id, message_0, channel_0_id, -1)


def test_message_share_not_joing_dm():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First0", "Last0")['token']
    token_1 = auth_register_v2("test_email1@gmail.com", "password", "First1", "Last1")['token']
    token_2 = auth_register_v2("test_email2@gmail.com", "password", "First2", "Last2")['token']
    auth_login_v1("test_email2@gmail.com", "password")
    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")['auth_user_id']
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")['auth_user_id']


    u_id_list = [u_id_0, u_id_1]
    dm_0_id = dm_create_v1(token_0, u_id_list)['dm_id']
    og_message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages['messages'][0]['message']

    with pytest.raises(AccessError):
        message_share_v1(token_2, og_message_0_id, message_0, -1, dm_0_id)


def test_message_share_channel_dm_id_both():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First0", "Last0")['token']
    auth_login_v1("test_email0@gmail.com", "password")
    token_1 = auth_register_v2("test_email1@gmail.com", "password", "First1", "Last1")['token']
    auth_login_v1("test_email1@gmail.com", "password")

    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    og_message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages['messages'][0].message

    with pytest.raises(InputError):
        message_share_v1(token_1, og_message_0_id, message_0, -1, -1)


#dm_id and channel_id are both -1
def test_message_share_channel_dm_id_both_not():
    clear_v1()
    token_0 = auth_register_v2("test_email0@gmail.com", "password", "First0", "Last0")['token']
    token_1 = auth_register_v2("test_email1@gmail.com", "password", "First1", "Last1")['token']
    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")['auth_user_id']
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")['auth_user_id']

    u_id_list = [u_id_0, u_id_1]
    dm_0_id = dm_create_v1(token_0, u_id_list)['dm_id']
    channel_0_id = channels_create_v1(token_0, 'channel_0', True)['channel_id']
    og_message_0_id = message_send_v2(token_0, channel_0_id, 'Hope it works')['message_id']

    all_messages = channel_messages_v1(token_0, channel_0_id, 0)
    message_0 = all_messages['messages'][0].message

    with pytest.raises(InputError):
        message_share_v1(token_1, og_message_0_id, message_0, channel_0_id, dm_0_id)
