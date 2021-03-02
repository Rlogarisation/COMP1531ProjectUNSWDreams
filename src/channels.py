from .data_file import Channel, data
from .error import InputError
from .other import clear_v1
from .auth import auth_login_v1, auth_register_v1, get_user_by_auth_id
from .channel import get_channel_by_channel_id


def channels_list_v1(auth_user_id):
    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }


def channels_listall_v1(auth_user_id):
    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }


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
