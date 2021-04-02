from datetime import timezone, datetime
<<<<<<< HEAD
from src.data_file import data, Message
from src.error import InputError, AccessError
from src.auth import get_user_by_token
from src.channel import get_channel_by_channel_id
=======
import json
import re
from src.data_file import data, Message, Permission
from src.error import InputError, AccessError
from src.auth import get_user_by_token, get_user_by_handle
from src.channel import get_channel_by_channel_id, is_user_owner_channel, is_user_in_channel
from src.dm import is_user_owner_dm, get_dm_by_dm_id, is_user_in_dm
from src.other import Notification
>>>>>>> master

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
    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user is None:
        raise AccessError(description='message_send_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_send_v2 : Message is more than 1000 characters.')

    # AccessError 1: invalid channel_id
    channel = get_channel_by_channel_id(channel_id)
    if type(channel_id) != int or channel is None:
        raise InputError(description='message_send_v2 : Invalid channel_id.')

    # AccessError 2: the authorised user has not joined the channel they are trying to post to
    if auth_user not in channel.all_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    new_message_id = create_message_id()
    time_created = datetime.utcnow().isoformat()
    message_created = Message(new_message_id, auth_user.u_id, message, time_created, channel.channel_id, -1)
    channel.messages.append(message_created)

    # check and tag user
    tagging_user(message, channel_id, -1, auth_user)

    return {
        'message_id': new_message_id,
    }

"""
Author: Shi Tong Yuan

message/senddm/v1

Background:
Send a message from authorised_user to the DM specified by dm_id. Note: Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel or DM.

Parameters: (token, dm_id, message)
Return Type: { message_id }
HTTP Method: POST

InputError:
    - (Added) Invalid token.
    - Message is more than 1000 characters
AccessError:
    - (Added) Invalid channel_id
    - the authorised user has not joined the channel they are trying to post to

"""


def message_senddm_v1(token, dm_id, message):
    # InputError 1: invalid token.
    auth_user = get_user_by_token(token)
    if auth_user is None:
        raise AccessError(description='message_send_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_send_v2 : Message is more than 1000 characters.')

    # AccessError 1: invalid dm_id
    dm = get_dm_by_dm_id(dm_id)
    if type(dm_id) != int or dm is None:
        raise InputError(description='message_send_v2 : Invalid dm_id.')

    # AccessError 2: the authorised user has not joined the channel they are trying to post to
    if auth_user not in dm.dm_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    new_message_id = create_message_id()
    created_time = datetime.utcnow().isoformat()
    message_created = Message(new_message_id, auth_user.u_id, message, created_time, -1, dm.dm_id)

    dm.dm_messages.append(message_created)

    # check and tag user
    tagging_user(message, -1, dm_id, auth_user)

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
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def message_senddm_v1(token, dm_id, message):
    # InputError 1: invalid token.
    try:
        auth_user = get_user_by_token(token)
    except:
        raise InputError(description='message_send_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_send_v2 : Message is more than 1000 characters.')

    # AccessError 1: invalid dm_id
    dm = get_dm_by_dm_id(dm_id)
    if type(dm_id) != int or dm == None:
        raise AccessError(description='message_send_v2 : Invalid channel_id.')

    # AccessError 2: the authorised user has not joined the channel they are trying to post to
    if auth_user not in dm.dm_members:
        raise AccessError(description='message_send_v2 : the authorised user has not joined the channel.')

    new_message_id = len(dm.dm_messages)
    message_created = Message(new_message_id, auth_user.u_id, message, datetime.utcnow(), -1, dm.dm_id)

    dm.dm_messages.append(message_created)

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
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def message_edit_v2(token, message_id, message):

    # InputError 1: invalid token.
    try:
        auth_user = get_user_by_token(token)
    except:
        raise InputError(description='message_edit_v2 : Invalid token.')

    # InputError 1: Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='message_edit_v2 : Message is more than 1000 characters.')

    # AccessError 1: Message editted by neither auth_user nor owner.
    if auth_user.u_id != get_u_id_by_message_id(message_id):
        raise AccessError(description='message_edit_v2 : Message editted by neither auth_user nor owner.')

    # Case 1: if new message is empty string, delete it
    if message == "":
        message_remove_v1(token, message_id)
    # Case 2: else edit message
    else:
        get_message_by_message_id(message_id).message = message

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
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

"""


def message_remove_v1(token, message_id):
    # InputError 1: invalid token.
    try:
        auth_user = get_user_by_token(token)
    except:
        raise InputError(description='message_remove_v1 : Invalid token.')

    # InputError 2: Message (based on ID) no longer exists
    target_message = get_message_by_message_id(message_id)
    if target_message == None:
        raise InputError(description='message_remove_v1 : Message (based on ID) no longer exists.')

    # AccessError 1: Message removed by neither auth_user nor owner.
    if auth_user.u_id != get_u_id_by_message_id(message_id):
        raise AccessError(description='message_remove_v1 : Message removed by neither auth_user nor owner.')

    # TODO:
    delete_message_by_message_id(message_id)

    return {}


"""
Author: Shi Tong Yuan

message/share/v1

Background:
og_message_id is the original message. channel_id is the channel that the message is being shared to, and is -1 if it is being sent to a DM. dm_id is the DM that the message is being shared to, and is -1 if it is being sent to a channel. message is the optional message in addition to the shared message, and will be an empty string '' if no message is given

Parameters: (token, og_message_id, message, channel_id, dm_id)
Return Type: {shared_message_id}
HTTP Method: POST

InputError:
    - (Added) if neither channel_id nor dm_id is -1 or both are -1

AccessError: 
    - the authorised user has not joined the channel or DM they are trying to share the message to

"""


def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    if channel_id == -1 and dm_id != -1:
        mem_list = get_dm_by_dm_id(dm_id).dm_members
    elif channel_id != -1 and dm_id == -1:
        mem_list = get_channel_by_channel_id(channel_id).all_members
    elif channel_id != -1 and dm_id != -1:
        raise InputError(description="message_share_v1 : neither channel_id nor dm_id is -1.")
    elif channel_id == -1 and dm_id == -1:
        raise InputError(description="message_share_v1 : both channel_id and dm_id is -1.")
    else:
        raise InputError(description="message_share_v1 : invalid input.")

    user = get_user_by_token(token)
    if user not in mem_list:
        raise AccessError(description="message_share_v1 : user need to be authorized.")

    og_message = get_message_by_message_id(og_message_id)
    message_added = ''.join([og_message.message, '\n"""\n', message, '\n"""'])
    # add og_message to new_message
    new_message = Message(create_message_id(), user.u_id, message_added, datetime.utcnow(), channel_id, dm_id)

    return {new_message.message_id}


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

def get_u_id_by_message_id(message_id):
    return get_message_by_message_id(message_id).u_id

def get_message_by_message_id(message_id):
    for i in data['class_channels']:
        for j in i.messages:
            if j.message_id == message_id:
                return j
    for i in data['class_dms']:
        for j in i.dm_messages:
            if j.message_id == message_id:
                return j
    raise InputError(description="get_message_by_message_id : can not find target message.")


def get_channel_dm_by_message_id(message_id):
    for i in data['class_channels']:
        for j in i.messages:
            if j.message_id == message_id:
                return [i, 0]
    for i in data['class_dms']:
        for j in i.dm_messages:
            if j.message_id == message_id:
                return [i, 1]
    return None

def delete_message_by_message_id(message_id):
    target_msg = get_message_by_message_id(message_id)
    for i in data['class_channels']:
        for j in i.messages:
            if j.message_id == target_msg.message_id:
                i.messages.remove(j)
                return
    for i in data['class_dms']:
        for j in i.dm_messages:
            if j.message_id == target_msg.message_id:
                i.dm_messages.remove(j)
                return
    raise AccessError(description="delete_message_by_message_id : can not find target message.")


def tagging_user(message, channel_id, dm_id, sender):
    channel = None
    dm = None
    if channel_id != -1:
        channel = get_channel_by_channel_id(channel_id)
        if channel is None:
            return None

    if dm_id != -1:
        dm = get_dm_by_dm_id(dm_id)
        if dm is None:
            return None

    if len(message) >= 20:
        first_20_char = message[:21]
    else:
        first_20_char = message[:]
    first_20_char = ''.join(first_20_char)

    split_msg = message.split()
    for word in split_msg:
        if re.search('@', word):
            handle = word[1:]
            invitee = get_user_by_handle(handle)
            if invitee is None:
                continue

            if channel_id != -1:
                if is_user_in_channel(channel_id, invitee.u_id) is None:
                    continue
                # add notification
                notification_message = f"{sender.handle_str} tagged you in {channel.name}: {first_20_char}"
                notification = Notification(channel.channel_id, -1, notification_message)
                invitee.notifications.append(notification)

            if dm_id != -1:

                if is_user_in_dm(dm, invitee.u_id) is None:
                    continue
                # add notification
                notification_message = f"{sender.handle_str} tagged you in {dm.dm_name}: {first_20_char}"
                notification = Notification(-1, dm_id, notification_message)
                invitee.notifications.append(notification)
