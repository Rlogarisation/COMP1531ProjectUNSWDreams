# channels.py is used to implement the functions for channels
# including channels_list and chennels_listall
# for 21T1 COMP1531 project
# Written by Zheng Luo (z5206267@ad.unsw.edu.au) on 02/Mar/2021
# Written by Lan (channels_create_v1)


from src.auth import auth_login_v1, auth_register_v1, get_user_by_auth_id, session_to_token, token_to_session, \
    get_user_by_token
from src.error import InputError, AccessError
from src.data_file import Channel, data

#############################################################################
#                                                                           #
#                               Channels_list_v1                            #
#                                                                           #
#############################################################################
"""
Author: Zheng Roger Luo
Background :
Provide a list of all channels (both public and private channels)
(and their associated details) that the authorised user is part of.

Parameters:(auth_user_id)
Return Type:{channels}

"""


def channels_list_v1(token):
    # Pull the data of user from data_file
    user = get_user_by_token(token)
    # Call return_type_channel(self) in order to get dictionary return
    list_return = []
    for channel in user.part_of_channel:
        list_return.append(channel.return_type_channel())
    return {
        'channels': list_return
    }


#############################################################################
#                                                                           #
#                           Channels_listall_v1                             #
#                                                                           #
#############################################################################
"""
Author: Zheng Roger Luo
Background :
Provide a list of all channels (and their associated details) 
regardless who calls, or owns it.

Parameters:(auth_user_id)
Return Type:{channels}
"""


def channels_listall_v1(token):
    # Pull the data of user from data_file
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="user does not refer to a vaild user")
    list_return = []
    for i in data['class_channels']:
        list_return.append(i.return_type_channel())
    return {
        'channels': list_return
    }

#############################################################################
#                                                                           #
#                           channels_create_v1                             #
#                                                                           #
#############################################################################


"""
Author: Lan Lin
Background :
Creates a new channel with that name that is either a public or private channel

Parameters: auth_user_id, name, is_public
Return Type: { channel_id }
"""


def create_channel_id():
    channel_id = len(data['class_channels'])
    return channel_id


def channels_create_v1(token, name, is_public):
    # error check that the name is more than 20 characters
    if len(name) > 20:
        raise InputError(description='Error! Name is more than 20 characters')
    if not isinstance(is_public, bool):
        raise InputError(description='is_public has to be bool')
    # error check if the owner has registered
    owner = get_user_by_token(token)
    if owner is None:
        raise AccessError(description='The token is invalid, or the owner has not registered')

    # get the owner who creates the channel by auth_user_id
    channel_id = create_channel_id()
    channel = Channel(name, channel_id, is_public)
    data['class_channels'].append(channel)
    owner.part_of_channel.append(channel)
    owner.channel_owns.append(channel)
    channel.owner_members.append(owner)
    channel.all_members.append(owner)

    return {
        'channel_id': channel_id
    }






