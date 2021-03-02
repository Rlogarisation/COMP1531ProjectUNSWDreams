from .data_file import User, Channel, data
from .error import InputError, AccessError

# Function checking if channel exists in current data
# Return channel dictionary if it exists and if not return None
def get_channel_by_channel_id(channel_id):
    for channel in data["class_channels"]:
        if channel_id == channel.channel_id:
            return channel
            break
    return None

# Function checking if user exists in current data
# Return user dictionary if it exists and if not return None  
def get_user_by_u_id(u_id):
    for user in data["class_users"]:
        if u_id == user.u_id:
            return user
            break
    return None

# Function checking if user is a part of a specific channel outlined by a channel_id
# Return user dictionary if it exists and if not return None
def is_user_in_channel(channel_id, u_id):
    channel = get_channel_by_channel_id(channel_id)
    for user in channel.all_members:
        if u_id == user.u_id:
            return user
    return None

# Checks if function channel_invite_v1 will generate an error
def error_check (channel_id, u_id, auth_user_id):
    # Checking for InputError
    # error_test1 and error_test2 checks if channel and user is valid or not
    # if user or channel is invalid throw inputError
    error_test1 = get_channel_by_channel_id(channel_id)
    error_test2 = get_user_by_u_id(u_id)
    if error_test1 == None or error_test2 == None:
        raise(InputError)

    # Checking for AccessError
    # error_test3 checks if user inviting the other user is in the channel
    error_test3 = is_user_in_channel(channel_id, auth_user_id)
    if error_test3 == None:
        raise(AccessError)

# Function adding user into specified channel and adds that channel into user class
def add_user_into_channel (channel_id,u_id):
    user = get_user_by_u_id(u_id)
    channel = get_channel_by_channel_id(channel_id)
    user.part_of_channel.append(channel)
    channel.all_members.append(user)

    

def channel_invite_v1(auth_user_id, channel_id, u_id):
    """
    Author : Emir Aditya Zen

    Background
    channel_invite_v1 - Invites a user (with user id u_id) to join a channel with ID channel_id. 
                        Once invited the user is added to the channel immediately

    Parameters: (auth_user_id, channel_id, u_id)
    Return Type: {}

    InputError when any of:
        channel_id does not refer to a valid channel.
        u_id does not refer to a valid user

    AccessError when any of:
        the authorised user is not already a member of the channel
        
    """
    
    # Case 1 error checks
    # Checks for cases of InputError indicated by invalid channel_id or u_id
    # In addition, checks for cases of AccessError indicated by authorised user calling
    # channel_invite_v1 function into a channel he is not part in
    error_check(channel_id, u_id, auth_user_id)
    
    # Case 2 no error occurs but user invited is already part of channel
    # Expected outcome is channel_invite_v1 function will just ignore the second
    # invitation call
    if (is_user_in_channel(channel_id, u_id) != None):
        return {}
    
    # Case 3 succesfull function calling
    # Expected outcome is invited user is now a member of the channel specified
    add_user_into_channel (channel_id,u_id)

    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    """
    Author : Emir Aditya Zen

    Background
    channel_invite_v1 - Given a Channel with ID channel_id that the authorised user 
                        is part of, provide basic details about the channel

    Parameters: (auth_user_id, channel_id)
    Return Type: {name, owner_members, all_members}

    InputError when any of:
        channel_id does not refer to a valid channel.

    AccessError when any of:
        Authorised user is not a member of channel with channel_id
        
    """
    # Case 1 InputError checks
    # Checks for cases of InputError indicated by invalid channel_id 
    input_error_test = get_channel_by_channel_id(channel_id)
    if input_error_test == None:
        raise(InputError)

    # Case 2 AccessError checks
    # Checks for cases of AccessError indicated by authorised user calling
    # channel_invite_v1 function into a channel he is not part in
    access_error_test = is_user_in_channel(channel_id, auth_user_id)
    if access_error_test == None:
        raise(AccessError)

    # Case 3 succesfull function calling
    # Expected outcome is function return basic details on the channel 
    # he/she is in through a dictionary form
    channel = get_channel_by_channel_id(channel_id)

    return {
        'name': channel.name,
        'owner_members': channel.owner_members,
        'all_members': channel.all_members,
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
