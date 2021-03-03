# channels.py is used to implement the functions for channels
# including channels_list and chennels_listall
# for 21T1 COMP1531 project
# Written by Zheng Luo (z5206267@ad.unsw.edu.au) on 02/Mar/2021


from .auth import auth_login_v1, auth_register_v1, get_user_by_auth_id
from .channel import get_channel_by_channel_id
from .error import InputError
from .data_file import Channel, data
from .other import clear_v1


#############################################################################
#                                                                           #
#                               Channels_list_v1                            #
#                                                                           #
#############################################################################
"""
channels_list():

Provide a list of all channels 
(and their associated details) that the authorised user is part of.

Parameters:(auth_user_id)
Return Type:{channels}

"""


def channels_list_v1(auth_user_id):

    # Pull the data of user from data_file
    user = get_user_by_auth_id(auth_user_id)

    # Call return_type_channel(self) in order to get dictionary return
    list_return = []
    for channel in user.part_of_channel:
        if (channel.is_public == True):
            list_return.append(channel.return_type_channel())
    return list_return

#############################################################################
#                                                                           #
#                           Channels_listall_v1                             #
#                                                                           #
#############################################################################
"""
channels_listall_v1:

Provide a list of all channels (and their associated details)
Explaination:
channel_listall_v1 should list all channels, 
including those that are private, regardless of who calls it.

Parameters:(auth_user_id)
Return Type:{channels}
"""



def channels_listall_v1(auth_user_id):
    # Pull the data of user from data_file
    user = get_user_by_auth_id(auth_user_id)

    # Call return_type_channel(self) in order to get dictionary return
    list_return = []
    for channel in user.part_of_channel:
        list_return.append(channel.return_type_channel())
    return list_return




def create_channel_id():
    channel_id = len(data['class_channels'])
    return channel_id



def create_channel_id():
    channel_id = len(data['class_channels'])
    return channel_id


def channels_create_v1(auth_user_id, name, is_public):
    # error check that the name is more than 20 characters
    if len(name) > 20:
        raise InputError('Error! Name is more than 20 characters')
    if not isinstance(is_public, bool):
        raise InputError('is_public has to be bool')
    # error check if the owner has registered
    owner = get_user_by_auth_id(auth_user_id)
    if owner is None:
        raise InputError('The owner has not registered')
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






