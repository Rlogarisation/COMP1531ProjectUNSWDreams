import random, pytest
from src import other, auth, channels, channel, error, data_file


def test_channel_messages_v1(auth_user_id, channel_id, start):
    pass


def test_channel_join_v1():
    # clear all previous changes
    other.clear_v1()

    # create the owner for testing
    auth.auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    owner = auth.auth_login_v1("TheOwner@test.com", "thisispassword")
    assert type(owner) is dict
    owner_u_id = owner["u_id"]
    owner_token = owner["token"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_token) is str

    # create the accesser for joining and leaving
    auth.auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")
    joiner = auth.auth_login_v1("TheJoiner@test.com", "joinerpassword")
    assert type(joiner) is dict
    joiner_u_id = joiner["u_id"]
    joiner_token = joiner["token"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_token) is str
    # create testing channel
    channel_id = channels.channels_create_v1(owner_token, "Testing Channel", True)
    assert channel_id is not None
    assert type(channel_id) is int

    def test_channel_join_normal():
        # Test for correctly executed
        assert channel.channel_join_v1(joiner_token, channel_id) == None

    def test_invalid_channel_id():
        # Test for invalid channel id
        invalid_id = random.randint(0, 10)
        with pytest.raises(error.InputError):
            channel.channel_join_v1(joiner_token, invalid_id)

    def test_join_private_channel():
        with pytest.raises(error.AccessError):
            channel.channel_join_v1(joiner_token, channel_id)

    pass