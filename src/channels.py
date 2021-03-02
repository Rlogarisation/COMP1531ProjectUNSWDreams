# channels.py is used to implement the functions for channels
# including channels_list and chennels_listall
# for 21T1 COMP1531 project
# Written by Zheng Luo (z5206267@ad.unsw.edu.au) on 02/Mar/2021


from .auth import get_user_by_auth_id
from .data_file import User, data



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
        if (channel.is_public == True) {
            list_return.append(channel.return_type_channel)
        }
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






def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }


