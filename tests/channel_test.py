import random, pytest
from src import other, auth, channels, channel, error, data_file


"""
channel_messages_v1()
Description:
Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

Error:
1. InputError
- invalid channel id
- start is greater than the total number of messages in the channel

2. AccessError
- the auth user is not in this channel.

"""


def msg_send(channel_id, msg_id, u_id, msg, time):
    message = {
        "message_id": msg_id,
        "u_id": u_id,
        "message": msg,
        "time_created": time,
    }

    for i in data_file.data["class_channels"]:
        if i["channel_id"] == channel_id:
            i.message.insert(0, message)
            break
    return


def test_channel_messages_v1(auth_user_id, channel_id, start):
    def test_invalid_channel_id():
        other.clear_v1()

        # create 2 users
        user1 = auth.auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
        user1 = auth.auth_login_v1("user1@test.com", "user1password")

        user2 = auth.auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
        user2 = auth.auth_login_v1("user2@test.com", "user2password")

        # create channel for testing
        Testing_channel_id = channels.channels_create_v1(user1["token"], "channel_test", True)
        channel.channel_invite_v1(user1["token"], Testing_channel_id, user2["u_id"])

        # testing for channel message function for invalid channel id inputError
        with pytest.raises(error.InputError("test_invalid_channel_id failed!!")):
            channel.channel_messages_v1(user1["token"], Testing_channel_id, 10)
        pass

    def test_auth_missing():
        other.clear_v1()

        # create 2 users and author people
        user1 = auth.auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
        user1 = auth.auth_login_v1("user1@test.com", "user1password")

        user2 = auth.auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
        user2 = auth.auth_login_v1("user2@test.com", "user2password")

        user3 = auth.auth_register_v1("user3@test.com", "user3password", "ShiTong", "Yuan")
        user3 = auth.auth_login_v1("user3@test.com", "user3password")

        # create channel by user1 for testing
        Testing_channel_id = channels.channels_create_v1(user1["token"], "channel_test", True)
        channel.channel_invite_v1(user1["token"], Testing_channel_id, user2["u_id"])

        # testing for channel message function for invalid channel id inputError
        with pytest.raises(error.InputError("test_auth_missing failed!!")):
            channel.channel_messages_v1(user3["token"], Testing_channel_id, 0)
        pass

    def test_no_msg():
        other.clear_v1()

        # create 2 users
        user1 = auth.auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
        user1 = auth.auth_login_v1("user1@test.com", "user1password")

        user2 = auth.auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
        user2 = auth.auth_login_v1("user2@test.com", "user2password")

        # create channel for testing
        Testing_channel_id = channels.channels_create_v1(user1["token"], "channel_test", True)
        channel.channel_invite_v1(user1["token"], Testing_channel_id, user2["u_id"])

        # 1. return -1 : for no more message after start
        message_stored = channel.channel_messages_v1(user1["token"], Testing_channel_id, 0).message
        assert message_stored == None, "test_no_msg failed!!"

    def test_less_than_50_msg():
        other.clear_v1()

        # create 2 users
        user1 = auth.auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
        user1 = auth.auth_login_v1("user1@test.com", "user1password")

        user2 = auth.auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
        user2 = auth.auth_login_v1("user2@test.com", "user2password")

        # create channel for testing
        Testing_channel_id = channels.channels_create_v1(user1["token"], "channel_test", True)

        # send testing message into channel chat
        for i in range(1, 3):
            msg_send(Testing_channel_id, i, user1["token"], "testing message", i)

        # FIXME:
        # 这边data_file里面没有start 和 end，对message的首尾无法定位
        # check_msg_amount = channel.channel_messages_v1(user1['token'], Testing_channel_id, 0)

        # assert(check_msg_amount[])

        # # 1. return -1 : for no more message after start
        # message_stored = channel.channel_messages_v1(user1["token"], Testing_channel_id, 0).message
        # assert len(message_stored) == 50

    def test_more_than_50_msg():
        pass

    pass


"""
channel_join_v1()
Description:
Given a channel_id of a channel that the authorised user can join, adds them to that channel


Error:
1. InputError
- Channel ID is not a valid channel

2. AccessError
- channel_id refers to a channel that is private (when the authorised user is not a global owner)

"""


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

    # ====================Testing=====================

    def test_channel_join_normal():
        # Test for correctly executed
        assert channel.channel_join_v1(joiner_token, channel_id) == None, "test_channel_join_normal failed!!"

    def test_invalid_channel_id():
        # Test for invalid channel id
        invalid_id = random.randint(0, 10)
        with pytest.raises(error.InputError("test_invalid_channel_id failed!!")):
            channel.channel_join_v1(joiner_token, invalid_id)

    def test_join_private_channel():
        with pytest.raises(error.AccessError("test_join_private_channel failed!!")):
            channel.channel_join_v1(joiner_token, channel_id)

    # ====================Testing=====================
    test_channel_join_normal()
    test_invalid_channel_id()
    test_join_private_channel()
    pass