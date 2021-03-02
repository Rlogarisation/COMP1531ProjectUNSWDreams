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
            channel_id_re = channel.channel_id
            channel_name_re = channel.name
            dict_re = {
                'channel_id': channel_id_re,
                'name': channel_name_re
            }
            list_return.append(dict_re)

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
    listall_return = []
    for channel in user.part_of_channel:
        listall_return.append(channel.return_type_channel)
    return listall_return




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


if __name__ == '__main__':
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    login = auth_login_v1('haha@gmail.com', '123123123')
    auth_user_id = login['auth_user_id']
    owner = get_user_by_auth_id(auth_user_id)

    channel1_id = channels_create_v1(auth_user_id, "public_channel", True)['channel_id']
    channel2_id = channels_create_v1(auth_user_id, "private_channel", False)['channel_id']

    channel1 = get_channel_by_channel_id(channel1_id)
    channel2 = get_channel_by_channel_id(channel2_id)
    assert channel2 is not None
    # print(f"len is {len(owner.part_of_channel)}")
    # print('hah')
    # print(channel1.name)
    # print('hah')
    # print(owner.part_of_channel[1].name)
    #
    # print(owner.part_of_channel)

    assert channel1 in owner.part_of_channel
    assert channel2 in owner.part_of_channel
    assert len(owner.part_of_channel) == 2
    assert channel1 in owner.channel_owns
    assert channel2 in owner.channel_owns
    assert len(owner.channel_owns) == 2

    assert owner in channel1.all_members
    assert owner in channel1.owner_members
    assert owner in channel2.all_members
    assert owner in channel2.owner_members



