from typing import Dict
from src.data_file import DATA, DM
from src.error import InputError, AccessError
from src.auth import get_user_by_auth_id, session_to_token, token_to_session, get_user_by_token, get_user_by_uid


#############################################################################
#                                                                           #
#                           Interface function                              #
#                                                                           #
#############################################################################

"""
Author: Zheng Luo

dm/create/v1

Background:
[u_id] is the user(s) that this DM is directed to, and will not include the creator. The creator is the owner of the DM. name should be automatically generated based on the user(s) that is in this dm. The name should be an alphabetically-sorted, comma-separated list of user handles, e.g. 'handle1, handle2, handle3'.

Parameters: (token, [u_id])
Return Type: { dm_id, dm_name }
HTTP Method: POST

InputError when any of:
u_id does not refer to a valid user

"""


def create_dm_id():
    dm_id = len(DATA['class_dms'])
    return dm_id


def dm_create_v1(token, u_id_list):

    list_dm_handles = []
    list_dm_invitee = []

    for uid in u_id_list:
        invitee = get_user_by_uid(uid)
        # input error if u_id does not refer to a valid user
        if invitee is None:
            raise InputError(description='The u_id is invalid, u_id does not refer to a vaild user')

        list_dm_invitee.append(invitee)
        list_dm_handles.append(invitee.handle_str)

    # input error if token does not refer to a valid token
    inviter = get_user_by_token(token)
    if inviter is None:
        raise InputError(description='The token is invalid, or the inviter has not registered')

    dm_name = ", ".join(list_dm_handles)
    dm_id = create_dm_id()

    dm = DM(dm_name, dm_id)
    # Update DATA
    DATA['class_dms'].append(dm)

    # Update members and owners inside class DM
    # Note: inviter is also part of member.
    # As well as,
    # Update part_of_dm and dm_owns inside class User
    for invitee in list_dm_invitee:
        dm.dm_members.append(invitee)
        invitee.part_of_dm.append(dm)

    dm.dm_members.append(inviter)
    inviter.part_of_dm.append(dm)

    dm.dm_owners.append(inviter)
    inviter.dm_owns.append(dm)

    return {
        'dm_id': dm_id,
        'dm_name': dm_name,
    }


"""
Author: Zheng Luo

dm/invite/v1

Background:
Inviting a user to an existing dm

Parameters: (token, dm_id, u_id)
Return Type: {}
HTTP Method: POST

InputError when any of: 
          dm_id does not refer to an existing dm.
          u_id does not refer to a valid user. 
       
AccessError when: 
        the authorised user is already a member of the DM.

"""


def dm_invite_v1(token, dm_id, u_id):
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # Input error when u_id does not refer to a valid user.
    invitee = get_user_by_uid(u_id)
    if invitee is None:
        raise InputError(description="u_id does not refer to a valid or exising user")

    # Access error when the authorised user is not already a member of the DM.
    inviter = get_user_by_token(token)
    if inviter is None:
        raise AccessError(description="The authorised user is not already a member of the DM")

    # Expect invitee is not part of member yet
    if invitee not in dm.dm_members:
        dm.dm_members.append(invitee)
        invitee.part_of_dm.append(dm)

    return {}


"""
Author: Zheng Luo

dm/remove/v1

Background:
Remove an existing DM. This can only be done by the original creator of the DM.

Parameters: (token, dm_id)
Return Type: {}
HTTP Method: DELETE

InputError when:   
    dm_id does not refer to a valid DM 
    
AccessError when:  
    the user is not the original DM creator

"""


def dm_remove_v1(token, dm_id):
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # AccessError when the user is not the original DM creator.
    inviter = get_user_by_token(token)
    if inviter is None:
        raise AccessError(description="The authorised user is not already a member of the DM")
    elif inviter not in dm.dm_owners:
        raise AccessError(description="The user is not the original DM creator")

    # Remove the current dm for all users in User.part_of_channel and dm_owns
    # Then remove dm in DATA class
    for member in dm.dm_members:
        member.part_of_dm.remove(dm)

    for owner in dm.dm_owners:
        owner.dm_owns.remove(dm)

    DATA['class_dms'].remove(dm)

    return {
    }


"""
Author: Zheng Luo

dm/leave/v1

Background:
Given a DM ID, the user is removed as a member of this DM

Parameters: (token, dm_id)
Return Type: {}
HTTP Method: POST

InputError when any of:
    dm_id is not a valid DM
      
AccessError when
    Authorised user is not a member of DM with dm_id

"""


def dm_leave_v1(token, dm_id):
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # Access error when the authorised user is not already a member of the DM.
    leaver = get_user_by_token(token)
    if leaver is None:
        raise AccessError(description="The authorised user is not already a member of the DM")

    # Remove member from dm
    dm.dm_members.remove(leaver)
    leaver.part_of_dm.remove(dm)
    # Considering owner leaving dm
    if leaver in dm.dm_owners:
        dm.dm_owners.remove(leaver)
        leaver.dm_owns.remove(dm)
        # Then first availble person in member become owner
        dm_next_owner = dm.dm_members[0]
        dm.dm_owners.append(dm_next_owner)
        dm_next_owner.dm_owns(dm)

    return {

    }


"""
Author: Zheng Luo

dm/details/v1

Background:
Users that are part of this direct message can view basic information about the DM

Parameters: (token, dm_id)
Return Type: { name, members }
HTTP Method: GET

InputError when any of:
    DM ID is not a valid DM
      
AccessError when
    Authorised user is not a member of this DM with dm_id
"""


def dm_details_v1(token, dm_id):
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # Access error when the authorised user is not already a member of the DM.
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="The authorised user is not already a member of the DM")

    return {
        'name': dm.dm_name,
        'members': dm.dm_members,
    }


"""
Author: Zheng Luo

dm/list/v1

Background:
Returns the list of DMs that the user is a member of

Parameters: (token)
Return Type: { dms }
HTTP Method: GET

N/A
"""


def dm_list_v1(token):
    user = get_user_by_token(token)
    dms = {}
    for dm_belongs in user.part_of_dm:
        dms.append(dm_belongs)
    return dms


"""
Author: Zheng Luo

dm/messages/v1

Background:
Given a DM with ID dm_id that the authorised user is part of,
return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

Parameters: (token, dm_id, start)
Return Type: { messages, start, end }
HTTP Method: GET

InputError when any of:
    DM ID is not a valid DM

    start is greater than the total number of messages in the channel
      
AccessError when any of:
    Authorised user is not a member of DM with dm_id
"""


def dm_messages_v1(token, dm_id, start):
    # Input error when dm_id does not refer to an existing dm.
    dm = get_dm_by_dm_id(dm_id)
    if dm is None:
        raise InputError(description="dm_id does not refer to a valid or exising dm")

    # Input error when start is greater than the total number of messages in the channel
    if start > len(dm.dm_messages):
        raise InputError(description="start is greater than the total number of messages in the channel")

    # Access error when Authorised user is not a member of DM with dm_id
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="The authorised user is not already a member of the DM")

    return_message = []
    counter_start = len(dm.dm_messages) - start
    if counter_start - 50 >= 0:
        counter_end = counter_start - 50
        end = counter_start + 50
    else:
        counter_end = 0
        end = -1
    while (counter_start >= counter_end):
        return_message.append(dm.dm_messages[counter_start])
        counter_start -= 1

    return {
        'messages': return_message,
        'start': start,
        'end': end
    }


#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################

def get_dm_by_dm_id(dm_id):
    if dm_id >= len(DATA['class_dms']):
        return None
    elif DATA['class_dms'][dm_id]:
        return DATA['class_dms'][dm_id]
    else:
        return None
