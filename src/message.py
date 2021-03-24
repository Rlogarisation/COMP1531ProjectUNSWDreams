from datetime import timezone, datetime
from src.data_file import data, Message
from src.error import InputError, AccessError
from src.auth import get_user_by_token
from src.channel import get_channel_by_channel_id

#############################################################################
#                                                                           #
#                           Interface function                              #
#                                                                           #
#############################################################################

"""
Author: Shi Tong Yuan

message/send/v2

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


def message_send_v2(token, channel_id, message):
    # for i in data["class_channels"]:
    #     if i.channel_id == channel_id:
    #         i.messages.insert(0, message)
    #         break

    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user == None:
        raise InputError(description='message_send_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_send_v2 : Message is more than 1000 characters.')

    # AccessError 1: invalid channel_id
    channel = get_channel_by_channel_id(channel_id)
    if type(channel_id) != int or channel == None:
        raise AccessError(description='message_send_v2 : Invalid channel_id.')

    # AccessError 2: the authorised user has not joined the channel they are trying to post to
    if auth_user not in channel.all_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    new_message_id = len(channel.messages)
    message_created = Message(new_message_id, auth_user.u_id, message, datetime.utcnow(), channel.channel_id)

    channel.messages.append(message_created)

    return {
        'message_id': new_message_id,
    }


"""
Author: Shi Tong Yuan

message/edit/v2

Background:
Given a message, update its text with new text. If the new message is an empty string, the message is deleted.

Parameters: (token, message_id, message)
Return Type: {}
HTTP Method: PUT

InputError:
    - (Added) Invalid token.
    - Length of message is over 1000 characters message_id refers to a deleted message
AccessError:
    # FIXME: 这边意思是写反了么？为什么要非auth_user和owner能修改，不应该是只有auth_user和owner能改么？
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def message_edit_v2(token, message_id, message):

    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user == None:
        raise InputError(description='message_edit_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_edit_v2 : Message is more than 1000 characters.')

    # AccessError 1: Message editted by neither auth_user nor owner.
    if auth_user.u_id == get_u_id_by_message_id(message_id):
        raise AccessError(description='message_edit_v2 : Message editted by neither auth_user nor owner.')

    # Case 1: if message is empty string, delete it

    # Case 2: else edit message

    return {}


"""
Author: Shi Tong Yuan

message/remove/v1

Background:
Given a message_id for a message, this message is removed from the channel/DM

Parameters: (token, message_id)
Return Type: {}
HTTP Method: DELETE

InputError:
    - (Added) Invalid token.
    - Message (based on ID) no longer exists
AccessError:
    # FIXME: 这边意思是写反了么？为什么要非auth_user和owner能remove，不应该是只有auth_user和owner能remove么？
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def message_remove_v1(token, message_id):
    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user == None:
        raise InputError(description='message_remove_v1 : Invalid token.')

    # InputError 2: Message (based on ID) no longer exists
    target_message = get_message_by_message_id(message_id)
    if target_message == None:
        raise InputError(description='message_remove_v1 : Message (based on ID) no longer exists.')

    # AccessError 1: Message removed by neither auth_user nor owner.
    if auth_user.u_id == get_u_id_by_message_id(message_id):
        raise AccessError(description='message_remove_v1 : Message removed by neither auth_user nor owner.')

    # TODO:
    delete_message_by_message_id(message_id)

    return {
    }


"""
Author: Shi Tong Yuan

message/share/v1

Background:
og_message_id is the original message. channel_id is the channel that the message is being shared to, and is -1 if it is being sent to a DM. dm_id is the DM that the message is being shared to, and is -1 if it is being sent to a channel. message is the optional message in addition to the shared message, and will be an empty string '' if no message is given

Parameters: (token, og_message_id, message, channel_id, dm_id)
Return Type: {shared_message_id}
HTTP Method: POST

AccessError: 
    - the authorised user has not joined the channel or DM they are trying to share the message to

"""


def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    return {
    }


#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


# generate a new session id
def create_message_id():
    new_id = data['message_num']
    data['message_num'] = data['message_num'] + 1
    return new_id


# FIXME: 想要通过message_id得到u_id,需要遍历messages[]，但每个channel的messages都是从0开始，message_id必定有重复
# TODO: 用create_session_id来，保证每个channel里面的message_id不重复
def get_u_id_by_message_id(message_id):
    return 0


# TODO: 通过message_id获取目标message
def get_message_by_message_id(message_id):
    return None


# TODO:通过message_id删除message
def delete_message_by_message_id(message_id):
    return None
