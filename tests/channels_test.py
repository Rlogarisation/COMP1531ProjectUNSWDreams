import pytest
from src.channels import channels_create_v1
from src.error import InputError
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, get_user_by_auth_id
from src.channel import get_channel_by_channel_id


def test_channels_create_length_of_name():
    clear_v1()
    register = auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    auth_user_id = register['auth_user_id']
    # check the length of name is more than 20 characters
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, 'A name clearly more than 20 characters', True)


# check the channle is public or not
def test_channels_create_public_or_not():
    clear_v1()
    register = auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    auth_user_id = register['auth_user_id']

    public_channel_id = channels_create_v1(auth_user_id, "public_channel", True)['channel_id']
    private_channel_id = channels_create_v1(auth_user_id, "private_channel", False)['channel_id']
    assert private_channel_id == 1
    channel_public = get_channel_by_channel_id(public_channel_id)
    channel_private = get_channel_by_channel_id(private_channel_id)

    assert channel_public
    assert channel_private
    assert channel_public.is_public
    assert (channel_private.is_public is False)


# check the is_public is boolean or not
def test_channels_create_is_public_bool():
    clear_v1()
    register = auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    auth_user_id = register['auth_user_id']
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, 'good_channel', 'not_a_bool')


# test if the channel has been created successfully
def test_channels_create_valid():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    login = auth_login_v1('haha@gmail.com', '123123123')
    auth_user_id = login['auth_user_id']
    owner = get_user_by_auth_id(auth_user_id)

    channel1_id = channels_create_v1(auth_user_id, "public_channel", True)['channel_id']
    channel2_id = channels_create_v1(auth_user_id, "private_channel", False)['channel_id']

    channel1 = get_channel_by_channel_id(channel1_id)
    channel2 = get_channel_by_channel_id(channel2_id)

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




