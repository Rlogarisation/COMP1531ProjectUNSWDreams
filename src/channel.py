from src import data_file, error


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {}


def channel_details_v1(auth_user_id, channel_id):
    return {
        "name": "Hayden",
        "owner_members": [
            {
                "u_id": 1,
                "name_first": "Hayden",
                "name_last": "Jacobs",
            }
        ],
        "all_members": [
            {
                "u_id": 1,
                "name_first": "Hayden",
                "name_last": "Jacobs",
            }
        ],
    }


"""Return 50 messages between `start` and `start + 50`.

    Args:
        token: the token of authorised user.
        channel_id: the id of channel we need info.
        start: the message we want to grab next 50 messages.

    Returns:
        -1: for no more message after start.
        50:
            1. exist messages after start and no more than 50 messages.
            2. the exist messages after start more than 50, just return the top 50 ones.
        { messages, start, end }

    Raises:
        1. InputError
            - the channel id is invalid;
            - start is greater than the total number of messages in the channel.
        2. AccessError
            - the authorised user is not in this channel.
    """
def channel_messages_v1(auth_user_id, channel_id, start):
    # InputError : invalid auth_user_id
    auth_inside = False
    for i in data_file.data['class_users']:
        if i.auth_user_id == auth_user_id:
            auth_inside = True
            break
    assert auth_inside == True, "channel_join_v1 : invalid auth_user_id"

    # InputError : invalid channel_id
    validity = False
    for i in data_file.data['class_channel']:
        if i.channel_id == channel_id:
            validity = True
            break
    assert validity == True, "channel_messages_v1 : invalid channel_id !!"

    # InputError : auth is not in channel
    auth_inside = False
    if auth_user_id not in data_file.data['class_channel'][channel_id].owner_members:
        raise (error.InputError("channel_messages_v1 : auth is not in channel"))

    start_num = data_file.data['class_channel'][channel_id].start
    end_num = data_file.data['class_channel'][channel_id].end

    # InputError : the start >= total messages.
    num_msg = len(data_file.data['class_channel'][channel_id].message)
    if num_msg < start_num:
        raise (error.AccessError("channel_messages_v1 : the start >= total messages."))

    return_msg = []
    if num_msg > (start + 50):
        return_msg = data_file.data['class_channel'][channel_id].message[start_num:end_num+1]
    else:
        return_msg = data_file.data['class_channel'][channel_id].message[start_num:]

    return {
        "messages": return_msg,
        "start": start_num,
        "end": end_num,
    }


def channel_leave_v1(auth_user_id, channel_id):
    return {}


"""Join the user by his/her token into a channel by channel_id.

    Args:
        token: the token of user who is leaving.
        channel_id: the channel which user is leaving.

    Returns:
        None.

    Raises:
        1. InputError
            - the channel id is invalid;
        2. AccessError
            - the channel is PRIVATE.
"""
def channel_join_v1(auth_user_id, channel_id):
    # InputError : invalid auth_user_id
    auth_inside = False
    for i in data_file.data['class_users']:
        if i.auth_user_id == auth_user_id:
            auth_inside = True
            new_member = i
            break
    assert auth_inside == True, "channel_join_v1 : invalid auth_user_id"

    # InputError : invalid channel_id
    validity = False
    for i in data_file.data['class_channel']:
        if i.channel_id == channel_id:
            validity = True
            target_channel = i
            break
    assert validity == True, "channel_join_v1 : invalid channel_id !!"

    # AccessError : channel is private
    if data_file.data['class_channel'][channel_id].is_public !=  False:
        raise (error.AccessError("channel_join_v1 : channel is private"))

    target_channel.all_members.append(new_member)

    return None


def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {}


def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {}
