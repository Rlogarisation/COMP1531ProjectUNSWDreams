import pytest
from src.error import InputError, AccessError
from src.dm import dm_create_v1, dm_details_v1, dm_invite_v1, dm_leave_v1, dm_list_v1, dm_messages_v1, dm_remove_v1
from src.auth import auth_register_v1, auth_login_v1, get_user_by_token
from src.other import clear_v1
#############################################################################
#                                                                           #
#                        Test for dm_details_v1                             #
#                                                                           #
#############################################################################
"""
dm_details_v1():

Users that are part of this direct message can view basic information about the DM.

Parameters:(token, dm_id)
Return Type:{ name, members }

TEST CASES:
	InputError when any of:
        DM ID is not a valid DM
    AccessError when
        Authorised user is not a member of this DM with dm_id

"""


def test_dm_details_v1():

    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    token2 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")['token']

    auth_id0 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id1 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    auth_id2 = auth_login_v1("user1@test.com", "user1password")["auth_user_id"]

    # user1 create the dm, invite user0 into dm
    dm_create_v1(token1, [0])

    # Case 1: DM ID is not a valid DM
    def test_invalid_dm():
        with pytest.raises(InputError):
            dm_details_v1(token1, "invalid_dm_id")
        pass

    # Case 2: Authorised user is not a member of this DM with dm_id
    def test_Inaccessible_member():
        # test: user2 should not be in dm, cause this is dm between user1 and user0
        with pytest.raises(AccessError):
            dm_details_v1(token2, 0)
        pass

    # --------------------------testing---------------------------
    test_invalid_dm()
    test_Inaccessible_member()
    pass


#############################################################################
#                                                                           #
#                         Test for dm_list_v1                               #
#                                                                           #
#############################################################################
"""
dm_list_v1():

Returns the list of DMs that the user is a member of.

Parameters:(token)
Return Type:{ dms }

TEST CASES:
	N/A

"""


def test_dm_list_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    token2 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")['token']

    auth_id0 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id1 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    auth_id2 = auth_login_v1("user1@test.com", "user1password")["auth_user_id"]

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    user0_involved = dm_list_v1(token0)

    assert user0_involved['dms'][0]['name'] == "peterwhite, tomgreen"
    assert user0_involved['dms'][0]['dm_id'] == 0

    assert user0_involved['dms'][1]['name'] == "peterwhite, rogerluo"
    assert user0_involved['dms'][1]['dm_id'] == 1

    pass


#############################################################################
#                                                                           #
#                        Test for dm_create_v1                              #
#                                                                           #
#############################################################################
"""
dm_create_v1():

[u_id] is the user(s) that this DM is directed to, and will not include the creator. The creator is the owner of the DM. name should be automatically generated based on the user(s) that is in this dm. The name should be an alphabetically-sorted, comma-separated list of user handles, e.g. 'handle1, handle2, handle3'.

Parameters:(token, [u_id])
Return Type:{ dm_id, dm_name }

TEST CASES:
	InputError when any of:
        u_id does not refer to a valid user

"""


def test_dm_create_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    token2 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")['token']

    auth_id0 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id1 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    auth_id2 = auth_login_v1("user1@test.com", "user1password")["auth_user_id"]

    def test_normal_case():
        dm1 = dm_create_v1(token0, [1])
        assert dm1['dm_id'] == 0
        assert dm1['dm_name'] == "peterwhite, tomgreen"
        pass

    def test_invalid_u_id():
        with pytest.raises(InputError):
            dm_create_v1(token1, [4, 5])
        pass

    # --------------------------testing---------------------------
    test_normal_case()
    test_invalid_u_id()
    pass


#############################################################################
#                                                                           #
#                        Test for dm_remove_v1                              #
#                                                                           #
#############################################################################
"""
dm_remove_v1():

Remove an existing DM. This can only be done by the original creator of the DM.

Parameters:(token, dm_id)
Return Type:{}

TEST CASES:
	InputError when:
        dm_id does not refer to a valid DM 
    AccessError when:
        the user is not the original DM creator

"""


def test_dm_remove_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    token2 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")['token']

    auth_id0 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id1 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    auth_id2 = auth_login_v1("user1@test.com", "user1password")["auth_user_id"]

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    def test_invalid_dm_id():
        with pytest.raises(InputError):
            dm_remove_v1(token0, "invalid_dm_id")
        pass

    def test_not_creator():
        with pytest.raises(AccessError):
            dm_remove_v1(token1, 1)
        pass

    # --------------------------testing---------------------------
    test_invalid_dm_id()
    test_not_creator()
    pass


#############################################################################
#                                                                           #
#                        Test for dm_invite_v1                              #
#                                                                           #
#############################################################################
"""
dm_invite_v1():

Inviting a user to an existing dm.

Parameters:(token, dm_id, u_id)
Return Type:{}

TEST CASES:
	InputError when any of:
        dm_id does not refer to an existing dm.
        u_id does not refer to a valid user.
    AccessError when:
        the authorised user is not already a member of the DM
"""


def test_dm_invite_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    token2 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")['token']

    auth_id0 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id1 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    auth_id2 = auth_login_v1("user1@test.com", "user1password")["auth_user_id"]

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    def test_invalid_dm_id():
        with pytest.raises(InputError):
            dm_invite_v1(token0, "invalid_dm_id", 2)
        pass

    def test_invalid_u_id():
        with pytest.raises(InputError):
            dm_invite_v1(token0, 0, "invalid_u_id")
        pass

    def test_already_user():
        with pytest.raises(AccessError):
            dm_invite_v1(token0, 0, 1)
        pass

    # --------------------------testing---------------------------
    test_invalid_dm_id()
    test_invalid_u_id()
    test_already_user()
    pass


#############################################################################
#                                                                           #
#                         Test for dm_leave_v1                              #
#                                                                           #
#############################################################################
"""
dm_leave_v1():

Given a DM ID, the user is removed as a member of this DM.

Parameters:(token, dm_id)
Return Type:{}

TEST CASES:
	InputError when any of:
        dm_id is not a valid DM
    AccessError when
        Authorised user is not a member of DM with dm_id

"""


def test_dm_leave_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    token2 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")['token']

    auth_id0 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id1 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    auth_id2 = auth_login_v1("user1@test.com", "user1password")["auth_user_id"]

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    def test_invalid_dm_id():
        with pytest.raises(InputError):
            dm_leave_v1(token0, "invalid_dm_id")
        pass

    def test_user_not_in():
        with pytest.raises(AccessError):
            dm_leave_v1(token0, 2)
        pass

    # --------------------------testing---------------------------
    test_invalid_dm_id()
    test_user_not_in()
    pass


#############################################################################
#                                                                           #
#                       Test for dm_messages_v1                             #
#                                                                           #
#############################################################################
"""
dm_messages_v1():

Given a DM with ID dm_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

Parameters:(token, dm_id, start)
Return Type:{ messages, start, end }

TEST CASES:
	InputError when any of:
        DM ID is not a valid DM
        start is greater than the total number of messages in the channel
    AccessError when any of:
        Authorised user is not a member of DM with dm_id

"""


def test_dm_messages_v1():
    clear_v1()
    token0 = auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")['token']
    token1 = auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")['token']
    token2 = auth_register_v1("user1@test.com", "user1password", "Roger", "Luo")['token']

    auth_id0 = auth_login_v1("haha@gmail.com", "123123123")["auth_user_id"]
    auth_id1 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")["auth_user_id"]
    auth_id2 = auth_login_v1("user1@test.com", "user1password")["auth_user_id"]

    dm_create_v1(token0, [1])
    dm_create_v1(token0, [2])
    dm_create_v1(token1, [2])

    def test_invalid_dm_id():
        with pytest.raises(InputError):
            dm_messages_v1(token0, "invalid_dm_id", 0)
        pass

    def test_oversized_start():
        with pytest.raises(InputError):
            dm_messages_v1(token0, 1, 999)
        pass

    def test_user_not_in():
        with pytest.raises(AccessError):
            dm_messages_v1(token1, 1, 0)
        pass

    # --------------------------testing---------------------------
    test_invalid_dm_id()
    test_oversized_start()
    test_user_not_in()
    pass
