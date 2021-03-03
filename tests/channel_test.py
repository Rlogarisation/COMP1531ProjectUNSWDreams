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
        if i.channel_id == channel_id:
            i.messages.insert(0, message)
            break
    return


def test_invalid_channel_id():
    other.clear_v1()

    # create 2 users
    user1 = auth.auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth.auth_login_v1("user1@test.com", "user1password")
    first_user = auth.get_user_by_auth_id(user1["auth_user_id"])

    user2 = auth.auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth.auth_login_v1("user2@test.com", "user2password")
    second_user = auth.get_user_by_auth_id(user2["auth_user_id"])

    # create channel for testing
    Testing_channel_id = channels.channels_create_v1(first_user.auth_user_id, "channel_test", True)
    channel.channel_invite_v1(first_user.auth_user_id, Testing_channel_id["channel_id"], second_user.u_id)

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(error.InputError):
        channel.channel_messages_v1(first_user.auth_user_id, Testing_channel_id["channel_id"], 10)


def test_auth_missing():
    other.clear_v1()

    # create 2 users and author people
    user1 = auth.auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth.auth_login_v1("user1@test.com", "user1password")
    first_user = auth.get_user_by_auth_id(user1["auth_user_id"])

    user2 = auth.auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth.auth_login_v1("user2@test.com", "user2password")
    second_user = auth.get_user_by_auth_id(user2["auth_user_id"])

    user3 = auth.auth_register_v1("user3@test.com", "user3password", "ShiTong", "Yuan")
    user3 = auth.auth_login_v1("user3@test.com", "user3password")

    # create channel by user1 for testing
    Testing_channel_id = channels.channels_create_v1(first_user.auth_user_id, "channel_test", True)
    channel.channel_invite_v1(first_user.auth_user_id, Testing_channel_id["channel_id"], second_user.u_id)

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(error.InputError):
        channel.channel_messages_v1(user3["auth_user_id"], Testing_channel_id["channel_id"], 0)


def test_no_msg():
    other.clear_v1()

    # create 2 users
    user1 = auth.auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth.auth_login_v1("user1@test.com", "user1password")
    first_user = auth.get_user_by_auth_id(user1["auth_user_id"])

    user2 = auth.auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth.auth_login_v1("user2@test.com", "user2password")
    second_user = auth.get_user_by_auth_id(user2["auth_user_id"])

    # create channel for testing
    Testing_channel_id = channels.channels_create_v1(first_user.auth_user_id, "channel_test", True)
    channel.channel_invite_v1(first_user.auth_user_id, Testing_channel_id["channel_id"], second_user.u_id)

    # 1. return -1 : for no more message after start
    message_stored = channel.channel_messages_v1(first_user.auth_user_id, Testing_channel_id["channel_id"], 0)["messages"]
    assert message_stored == [], "test_no_msg failed!!"


def test_less_than_50_msg():
    other.clear_v1()

    # create 2 users
    user1 = auth.auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth.auth_login_v1("user1@test.com", "user1password")

    user2 = auth.auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth.auth_login_v1("user2@test.com", "user2password")

    # create channel for testing
    Testing_channel_id = channels.channels_create_v1(user1["auth_user_id"], "channel_test", True)

    # send testing message into channel chat
    for i in range(1, 3):
        msg_send(Testing_channel_id["channel_id"], i, user1["auth_user_id"], "testing message", i)

    check_msg_amount = channel.channel_messages_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], 0)

    # 1. return -1 : for no more message after start
    message_stored = channel.channel_messages_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], 0)["messages"]
    assert len(message_stored) == 2


def test_more_than_50_msg():
    other.clear_v1()

    # create 2 users
    user1 = auth.auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth.auth_login_v1("user1@test.com", "user1password")

    user2 = auth.auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth.auth_login_v1("user2@test.com", "user2password")

    # create channel for testing
    Testing_channel_id = channels.channels_create_v1(user1["auth_user_id"], "channel_test", True)

    # send testing message into channel chat
    for i in range(1, 99):
        msg_send(Testing_channel_id["channel_id"], i, user1["auth_user_id"], "testing message", i)

    check_msg_amount = channel.channel_messages_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], 0)

    # 1. return -1 : for no more message after start
    message_stored = channel.channel_messages_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], 0)["messages"]
    assert len(message_stored) == 50


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


def test_channel_join_normal():
    # clear all previous changes
    other.clear_v1()

    # create the owner for testing
    auth.auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    owner = auth.auth_login_v1("TheOwner@test.com", "thisispassword")
    assert type(owner) is dict
    owner_u_id = auth.get_user_by_auth_id(owner["auth_user_id"]).u_id
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int

    # create the accesser for joining and leaving
    auth.auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")
    joiner = auth.auth_login_v1("TheJoiner@test.com", "joinerpassword")
    assert type(joiner) is dict
    joiner_u_id = auth.get_user_by_auth_id(joiner["auth_user_id"]).u_id
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int

    # create testing channel
    channel_id = channels.channels_create_v1(owner_auth_user_id, "Testing Channel", True)
    assert channel_id is not None
    assert type(channel_id["channel_id"]) is int

    # Test for correctly executed
    assert channel.channel_join_v1(joiner_auth_id, channel_id["channel_id"]) == {}, "test_channel_join_normal failed!!"


def test_invalid_channel_id():
    # clear all previous changes
    other.clear_v1()

    # create the owner for testing
    auth.auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    owner = auth.auth_login_v1("TheOwner@test.com", "thisispassword")
    assert type(owner) is dict
    owner_u_id = auth.get_user_by_auth_id(owner["auth_user_id"]).u_id
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int

    # create the accesser for joining and leaving
    auth.auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")
    joiner = auth.auth_login_v1("TheJoiner@test.com", "joinerpassword")
    assert type(joiner) is dict
    joiner_u_id = auth.get_user_by_auth_id(joiner["auth_user_id"]).u_id
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int

    # create testing channel
    channel_id = channels.channels_create_v1(owner_auth_user_id, "Testing Channel", True)
    assert channel_id is not None
    assert type(channel_id["channel_id"]) is int

    # Test for invalid channel id
    invalid_id = {"channel_id": random.randint(0, 10)}
    with pytest.raises(error.InputError):
        channel.channel_join_v1(joiner_auth_id, invalid_id["channel_id"])


def test_join_private_channel():
    # clear all previous changes
    other.clear_v1()

    # create the owner for testing
    auth.auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    owner = auth.auth_login_v1("TheOwner@test.com", "thisispassword")
    assert type(owner) is dict
    owner_u_id = auth.get_user_by_auth_id(owner["auth_user_id"]).u_id
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int

    # create the accesser for joining and leaving
    auth.auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")
    joiner = auth.auth_login_v1("TheJoiner@test.com", "joinerpassword")
    assert type(joiner) is dict
    joiner_u_id = auth.get_user_by_auth_id(joiner["auth_user_id"]).u_id
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int

    # create testing private channel
    channel_id_2 = channels.channels_create_v1(owner_auth_user_id, "Testing Channel_2", False)

    assert channel_id_2 is not None
    assert type(channel_id_2["channel_id"]) is int
    with pytest.raises(error.AccessError):
        channel.channel_join_v1(joiner_auth_id, channel_id_2["channel_id"])
