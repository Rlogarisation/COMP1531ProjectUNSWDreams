# Imports the necessary function implementations
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_join_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1
from src.message import message_send_v1

# Imports the possible error output
from src.error import InputError, AccessError

# Imports pytest
import pytest


"""
Author : Emir Aditya Zen

This file is for testing channel_invite_v1 function implementation

Background
Invites a user (with user id u_id) to join a channel with ID channel_id.
Once invited the user is added to the channel immediately

Parameters: (auth_user_id, channel_id, u_id)
Return Type: {}

InputError:
- channel_id does not refer to a valid channel.
- u_id does not refer to a valid user

AccessError:
- the authorised user is not already a member of the channel

"""
#############################################################################
#                                                                           #
#                       Test for channel_invite_v1                          #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is user gets invited to a channel and gets added to it
# Occurs when channel is valid and user is valid whilst having not been invited before
def test_channel_invite_v1_success():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    # register two users with valid inputs
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    login1 = auth_login_v1("haha@gmail.com", "123123123")
    login2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")

    # Identify user_id and auth_user_id for 2 registered user for testing

    user_1_id_auth = login1["auth_user_id"]
    user_2_id_auth = login2["auth_user_id"]
    user_2_id = user_2_id_auth

    # Create Channel_1 made by user_1 and get its id
    create_channel1 = channels_create_v1(user_1_id_auth, "channelone", True)
    Channel_1_id = create_channel1["channel_id"]

    # Calls invite function for testing
    # (user 1 invites user 2 into the channel he/she is in)
    channel_invite_v1(user_1_id_auth, Channel_1_id, user_2_id)

    # Expected output is user_2 joins the Channel_1

    # Hence checks that Channel_1 exists, has 2 members, and the members are
    # user_1 and user_2
    channel_members = channel_details_v1(user_1_id_auth, Channel_1_id)['all_members']
    user1 = channel_members[0]
    user2 = channel_members[1]
    assert user1['email'] == 'haha@gmail.com'
    assert user2['email'] == 'test@testexample.com'


# Case 2 - tests for repeated invite instances
#          expected outcome is recognizes user invited is already in the channel and does nothing
# Occurs when channel is valid and user is already inside the channel
def test_channel_invite_v1_repeated():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    auth_id1 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    user_2_id = auth_id2

    # Create Channel_1 made by user_1 and get its id
    Channel_1_id = channels_create_v1(auth_id1, "channelone", True)["channel_id"]

    # Calls invite function twice targeting the same user for testing repetition
    # (user 1 invites user 2 into the channel he/she is in twice)
    channel_invite_v1(auth_id1, Channel_1_id, user_2_id)
    channel_invite_v1(auth_id1, Channel_1_id, user_2_id)

    # Expected output is user_2 joins the Channel_1 on the first invite and
    # ignores the second invite

    # Hence checks that Channel_1 exists, has 2 members, and the members are
    # user_1 and user_2
    channel_members = channel_details_v1(auth_id1, Channel_1_id)['all_members']
    assert len(channel_members) == 2
    user1 = channel_members[0]
    user2 = channel_members[1]
    assert user1['email'] == 'haha@gmail.com'
    assert user2['email'] == 'test@testexample.com'


# Case 3 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel_id does not refer to a valid channel.
def test_channel_invite_v1_inputErrorChannel():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    auth_id1 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    user_2_id = auth_id2

    # Create Channel_1 made by user_1 and get its id
    Channel_1_id = channels_create_v1(auth_id1, "channelone", True)["channel_id"]

    # Made an invalid channel id for testing
    Channel_1_invalid_id = Channel_1_id + 300

    # Test conditions leading to an input error outcome due to invalid channel_id
    with pytest.raises(InputError):
        channel_invite_v1(auth_id1, Channel_1_invalid_id, user_2_id)


# Case 4 - tests for input error due to invalid user
#          expected outcome is input error
# Occurs when u_id does not refer to a valid user.
def test_channel_invite_v1_inputErrorUser():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    auth_id1 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    user_2_id = auth_id2

    # Create Channel_1 made by user_1 and get its id
    Channel_1_id = channels_create_v1(auth_id1, "channelone", True)["channel_id"]

    # Made an invalid user id for user 2
    user_2_id_invalid_id = user_2_id + 300

    # Test conditions leading to an input error outcome due to invalid u_id
    with pytest.raises(InputError):
        channel_invite_v1(auth_id1, Channel_1_id, user_2_id_invalid_id)


# Case 5 - tests for access error
#          expected outcome is access error
# Occurs when the authorised user is not already a member of the channel
# Meaning user 2 invites user 3 into a channel eventhough channel was made by user 1
def test_channel_invite_v1_accessError():
    # Clears data and registers and logins user_1, user_2, and user_3
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")
    auth_register_v1("hah2@gmail.com", "9uisbxh83h", "Tom", "Green")

    # login the two registered users
    auth_id1 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    auth_id3 = auth_login_v1("hah2@gmail.com", "9uisbxh83h")["auth_user_id"]
    user_3_id = auth_id3

    # Create Channel_1 made by user_1 and get its id
    Channel_1_id = channels_create_v1(auth_id1, "channelone", True)["channel_id"]

    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channel_invite_v1(auth_id2, Channel_1_id, user_3_id)


"""
Author : Emir Aditya Zen

This file is for testing channel_details_v1 function implementation

Background
Given a Channel with ID channel_id that the authorised user
is part of, provide basic details about the channel

Parameters: (auth_user_id, channel_id)
Return Type: {name, owner_members, all_members}

InputError:
- channel_id does not refer to a valid channel.

AccessError:
- Authorised user is not a member of channel with channel_id

"""
#############################################################################
#                                                                           #
#                       Test for channel_detail_v1                           #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation with a single group member
#          expected outcome is output of {name, owner_members, all_members}
# Occurs when channel is valid and there is only 1 member in that group
def test_channel_details_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    auth_id1 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    user_2_id = auth_id2

    # Create Channel_1 made by user_1 and get its id
    Channel_1_id = channels_create_v1(auth_id1, "channelone", True)["channel_id"]

    channel_invite_v1(auth_id1, Channel_1_id, user_2_id)
    # Calls details function for testing
    output = channel_details_v1(auth_id1, Channel_1_id)

    assert output["all_members"][0]["name_first"] == 'Peter'
    assert output["all_members"][1]["name_first"] == 'Tom'
    assert output["owner_members"][0]["name_first"] == 'Peter'
    assert output["name"] == "channelone"


# Case 3 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel_id does not refer to a valid channel.
def test_channel_details_v1_inputError():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    auth_id1 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    Channel_1_id = channels_create_v1(auth_id1, "channelone", True)["channel_id"]

    # Made an invalid channel id for testing
    Channel_1_invalidid = Channel_1_id + 300

    # Conditions leads to an input error outcome and tests for it
    with pytest.raises(InputError):
        channel_details_v1(auth_id1, Channel_1_invalidid)


# Case 4 - tests for access error
#          expected outcome is access error
# Occurs when the authorised user is not a member of channel with channel_id
def test_channel_details_v1_accessError():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    auth_id1 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]

    # Create Channel_1 made by user_1 and get its id
    Channel_1_id = channels_create_v1(auth_id1, "channelone", True)["channel_id"]

    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channel_details_v1(auth_id2, Channel_1_id)


"""
Author : Shi Tong Yuan

This file is for testing channel_messages_v1 function implementation

Background
Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

Parameters: (auth_user_id, channel_id, start)
Return Type: {messages, start, end}

InputError:
- Channel ID is not a valid channel
- start is greater than the total number of messages in the channel

AccessError:
- Authorised user is not a member of channel with channel_id

"""
#############################################################################
#                                                                           #
#                       Test for channel_messages_v1                        #
#                                                                           #
#############################################################################


def test_invalid_channel_id():
    clear_v1()

    # create 2 users
    user1 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    user2 = auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth_login_v1("user2@test.com", "user2password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["auth_user_id"], "channel_test", True)
    channel_invite_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], user2["auth_user_id"])

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(InputError):
        channel_messages_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], 10)


def test_auth_missing():
    clear_v1()

    # create 2 users and author people
    user1 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    user2 = auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth_login_v1("user2@test.com", "user2password")

    user3 = auth_register_v1("user3@test.com", "user3password", "ShiTong", "Yuan")
    user3 = auth_login_v1("user3@test.com", "user3password")

    # create channel by user1 for testing
    Testing_channel_id = channels_create_v1(user1["auth_user_id"], "channel_test", True)
    channel_invite_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], user2["auth_user_id"])

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(InputError):
        channel_messages_v1(user3["auth_user_id"], Testing_channel_id["channel_id"], 0)


def test_no_msg():
    clear_v1()

    # create 2 users
    user1 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    user2 = auth_register_v1("user2@test.com", "user2password", "Lan", "Lin")
    user2 = auth_login_v1("user2@test.com", "user2password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["auth_user_id"], "channel_test", True)
    channel_invite_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], user2["auth_user_id"])

    # 1. return -1 : for no more message after start
    message_stored = channel_messages_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], 0)["messages"]
    assert message_stored == [], "test_no_msg failed!!"


def test_less_than_50_msg():
    clear_v1()

    # create 2 users
    user1 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["auth_user_id"], "channel_test", True)

    # send testing message into channel chat
    for i in range(1, 3):
        message_send_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], "This is a testing message.")

    # 1. return -1 : for no more message after start
    message_stored = channel_messages_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], 0)["messages"]
    assert len(message_stored) == 2


def test_more_than_50_msg():
    clear_v1()

    # create 2 users
    user1 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")
    user1 = auth_login_v1("user1@test.com", "user1password")

    # create channel for testing
    Testing_channel_id = channels_create_v1(user1["auth_user_id"], "channel_test", True)

    # send testing message into channel chat
    for i in range(1, 99):
        message_send_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], "This is a testing message.")

    # 1. return -1 : for no more message after start
    message_stored = channel_messages_v1(user1["auth_user_id"], Testing_channel_id["channel_id"], 0)["messages"]
    assert len(message_stored) == 50


"""
Author : Shi Tong Yuan

This file is for testing channel_join_v1 function implementation

Background
Given a channel_id of a channel that the authorised user can join, adds them to that channel

Parameters: (auth_user_id, channel_id)
Return Type: {}

InputError:
- Channel ID is not a valid channel

AccessError:
- channel_id refers to a channel that is private (when the authorised user is not a global owner)

"""
#############################################################################
#                                                                           #
#                         Test for channel_join_v1                          #
#                                                                           #
#############################################################################


def test_channel_join_normal():
    # clear all previous changes
    clear_v1()

    # create the owner for testing
    auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    owner = auth_login_v1("TheOwner@test.com", "thisispassword")
    assert type(owner) is dict
    owner_u_id = owner["auth_user_id"]
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int

    # create the accesser for joining and leaving
    auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")
    joiner = auth_login_v1("TheJoiner@test.com", "joinerpassword")
    assert type(joiner) is dict
    joiner_u_id = joiner["auth_user_id"]
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int

    # create testing channel
    channel_id = channels_create_v1(owner_auth_user_id, "Testing Channel", True)
    assert channel_id is not None
    assert type(channel_id["channel_id"]) is int

    # Test for correctly executed
    assert channel_join_v1(joiner_auth_id, channel_id["channel_id"]) == {}, "test_channel_join_normal failed!!"


def test_invalid_channel_id():
    # clear all previous changes
    clear_v1()

    # create the owner for testing
    auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    owner = auth_login_v1("TheOwner@test.com", "thisispassword")
    assert type(owner) is dict
    owner_u_id = owner["auth_user_id"]
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int

    # create the accesser for joining and leaving
    auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")
    joiner = auth_login_v1("TheJoiner@test.com", "joinerpassword")
    assert type(joiner) is dict
    joiner_u_id = joiner["auth_user_id"]
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int

    # create testing channel
    channel_id = channels_create_v1(owner_auth_user_id, "Testing Channel", True)
    assert channel_id is not None
    assert type(channel_id["channel_id"]) is int

    # Test for invalid channel id
    invalid_id = {"channel_id": 999999}
    with pytest.raises(InputError):
        channel_join_v1(joiner_auth_id, invalid_id["channel_id"])


def test_join_private_channel():
    # clear all previous changes
    clear_v1()

    # create the owner for testing
    auth_register_v1("TheOwner@test.com", "thisispassword", "ShiTong", "Yuan")
    owner = auth_login_v1("TheOwner@test.com", "thisispassword")
    assert type(owner) is dict
    owner_u_id = owner["auth_user_id"]
    owner_auth_user_id = owner["auth_user_id"]
    assert owner_u_id is not None
    assert type(owner_u_id) is int
    assert type(owner_auth_user_id) is int

    # create the accesser for joining and leaving
    auth_register_v1("TheJoiner@test.com", "joinerpassword", "Roger", "Luo")
    joiner = auth_login_v1("TheJoiner@test.com", "joinerpassword")
    assert type(joiner) is dict
    joiner_u_id = joiner["auth_user_id"]
    joiner_auth_id = joiner["auth_user_id"]
    assert joiner_u_id is not None
    assert type(joiner_u_id) is int
    assert type(joiner_auth_id) is int

    # create testing private channel
    channel_id_2 = channels_create_v1(owner_auth_user_id, "Testing Channel_2", False)

    assert channel_id_2 is not None
    assert type(channel_id_2["channel_id"]) is int
    with pytest.raises(AccessError):
        channel_join_v1(joiner_auth_id, channel_id_2["channel_id"])
