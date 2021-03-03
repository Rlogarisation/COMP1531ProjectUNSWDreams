from typing import Dict
from .data_file import data
from .error import InputError, AccessError
from .auth import get_user_by_auth_id

# from data_file import Channel, data


def get_channel_by_channel_id(channel_id):
    # for channel in data['class_channels']:
    #     if channel_id == channel.channel_id:
    #         return channel
    #     else:
    #         return None

    if channel_id >= len(data["class_channels"]):
        return None
    elif data["class_channels"][channel_id]:
        return data["class_channels"][channel_id]
    else:
        return None


# Function checking if user exists in current data
# Return user dictionary if it exists and if not return None
def get_user_by_u_id(u_id):
    for user in data["class_users"]:
        if u_id == user.u_id:
            return user
    else:
        return None


def channel_messages_v1(auth_user_id, channel_id, start):
    if auth_user_id == -1:
        raise (InputError("channel_messages_v1: invalid token."))

    target_channel = get_channel_by_channel_id(channel_id)
    if target_channel == None:
        raise (InputError("channel_messages_v1: invalid channel_id."))

    # check if target user is in channel's members
    target_user = get_user_by_auth_id(auth_user_id)
    target_auth_user_id = target_user.auth_user_id
    user_inside = False
    for i in target_channel.all_members:
        if i.auth_user_id == target_auth_user_id:
            user_inside = True
            break
    if user_inside == False:
        raise (InputError("channel_messages_v1 : target user is not in channel"))

    num_msgs = len(target_channel.messages)
    if num_msgs < start:
        raise (InputError("channel_messages_v1 : the start >= total messages."))

    return_msg = []
    if num_msgs > (start + 50):
        return_msg = target_channel.messages[start : start + 50]
    else:
        return_msg = target_channel.messages[start:]

    return {
        "messages": return_msg,
        "start": target_channel.start,
        "end": target_channel.end,
    }


def channel_leave_v1(auth_user_id, channel_id):
    return {}


def channel_join_v1(auth_user_id, channel_id):
    target_channel = get_channel_by_channel_id(channel_id)

    if target_channel is None:
        raise (InputError("channel_join_v1 : invalid channel_id."))

    if target_channel.is_public is False:
        raise (AccessError("channel_join_v1 : channel is PRIVATE."))

    assert type(auth_user_id) is int
    if auth_user_id == -1:
        raise (InputError("channel_join_v1 : invalid auth_user_id"))

    new_member = get_user_by_auth_id(auth_user_id)

    for i in data["class_channels"]:
        if i.channel_id == channel_id:
            i.all_members.append(new_member)
            break

    return {}


def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {}


def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {}


# check if the user is a member of channel
def is_user_in_channel(channel_id, auth_user_id):
    channel = get_channel_by_channel_id(channel_id)
    for user in channel.all_members:
        if auth_user_id == user.auth_user_id:
            return user
    return None


# Checks if function channel_invite_v1 will generate an error
def error_check(channel_id, u_id, auth_user_id):
    # Checking for InputError
    # error_test1 and error_test2 checks if channel and user is valid or not
    # if user or channel is invalid throw inputError
    channel_ = get_channel_by_channel_id(channel_id)
    if channel_ is None:
        raise InputError("Channel_id does not refer to a valid channel")

    invitee = get_user_by_u_id(u_id)
    if invitee is None:
        raise InputError("u_id does not refer to a valid user")

    # Checking for AccessError
    # error_test3 checks if user inviting the other user is in the channel
    sender = is_user_in_channel(channel_id, auth_user_id)
    if sender is None:
        raise AccessError("The authorised user is not a member of the channel")


# Function adding user into specified channel and adds that channel into user class
def add_user_into_channel(channel, invitee):
    invitee.part_of_channel.append(channel)
    channel.all_members.append(invitee)


def channel_invite_v1(auth_user_id, channel_id, u_id):
    """
    Author : Emir Aditya Zen

    Background
    channel_invite_v1 - Invites a user (with user id u_id) to join a channel with ID channel_id.
                        Once invited the user is added to the channel immediately

    Parameters: (auth_user_id, channel_id, u_id)
    Return Type: {}

    InputError when any of:
        channel_id does not refer to a valid channel.
        u_id does not refer to a valid user

    AccessError when any of:
        the authorised user is not already a member of the channel

    """

    # Case 1 error checks
    # Checks for cases of InputError indicated by invalid channel_id or u_id
    # In addition, checks for cases of AccessError indicated by authorised user calling
    # channel_invite_v1 function into a channel he is not part in
    error_check(channel_id, u_id, auth_user_id)

    # Case 2 no error occurs but user invited is already part of channel
    # Expected outcome is channel_invite_v1 function will just ignore the second
    # invitation call
    invitee = get_user_by_u_id(u_id)
    channel = get_channel_by_channel_id(channel_id)
    if channel not in invitee.part_of_channel:
        # Case 3 succesfull function calling
        # Expected outcome is invited user is now a member of the channel specified
        add_user_into_channel(channel, invitee)

    return {}


def channel_details_v1(auth_user_id, channel_id):
    """
    Author : Emir Aditya Zen

    Background
    channel_invite_v1 - Given a Channel with ID channel_id that the authorised user
                        is part of, provide basic details about the channel

    Parameters: (auth_user_id, channel_id)
    Return Type: {name, owner_members, all_members}

    InputError when any of:
        channel_id does not refer to a valid channel.

    AccessError when any of:
        Authorised user is not a member of channel with channel_id

    """
    # Case 1 InputError checks
    # Checks for cases of InputError indicated by invalid channel_id
    channel = get_channel_by_channel_id(channel_id)
    if channel is None:
        raise InputError("Channel_id does not refer to a valid channel")

    # Case 2 AccessError checks
    # Checks for cases of AccessError indicated by authorised user calling
    # channel_invite_v1 function into a channel he is not part in
    sender = is_user_in_channel(channel_id, auth_user_id)
    if sender is None:
        raise AccessError("The authorised user is not a member of the channel")

    # Case 3 succesfull function calling
    # Expected outcome is function return basic details on the channel
    # he/she is in through a dictionary form
    owner_list = []
    member_list = []
    for owner in channel.owner_members:
        dict_owner = {"u_id": owner.u_id, "name_first": owner.name_first, "name_last": owner.name_last}
        owner_list.append(dict_owner)

    for member in channel.all_members:
        dict_member = {"u_id": member.u_id, "name_first": member.name_first, "name_last": member.name_last}
        member_list.append(dict_member)

    return {
        "name": channel.name,
        "owner_members": owner_list,
        "all_members": member_list,
    }
