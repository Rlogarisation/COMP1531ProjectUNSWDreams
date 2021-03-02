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
