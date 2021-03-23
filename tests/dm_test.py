import pytest

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
    pass
