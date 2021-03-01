"""
Author : Emir Aditya Zen

This file is for testing channel_details_v1 function implementation

Background
channel_invite_v1 - Given a Channel with ID channel_id that the authorised user 
                    is part of, provide basic details about the channel

Parameters: (auth_user_id, channel_id)
Return Type: {name, owner_members, all_members}

InputError when any of:
    channel_id does not refer to a valid channel.

AccessError when any of:
    Authorised user is not a member of channel with channel_id
    
TO DO
- finish case 1 and case 2
- check with group if channel_id is an int or a string
- check with group if u_id is an int or a string
- check with forup that channel name has to be a string or not
"""

# Imports the necessary function implementations
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, \
    channel_messages_v1, channel_join_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1

# Imports the possible error output
from src.error import InputError, AccessError

# Imports current global listed data
import src.data_file.py

# Imports pytest
import pytest

# Case 1 - tests for valid function implementation with a single group member
#          expected outcome is output of {name, owner_members, all_members}
# Occurs when channel is valid and there is only 1 member in that group
def test_channel_details_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    user_1 = auth_register_v1(user1@gmail.com, user1pass, numerouno, uno)
    user_1 = auth_login_v1(user1@gmail.com, user1pass)

    # Identify user_id and auth_user_id for registered user for testing
    user_1_id = user_1.u_id
    user_1_id_auth = user_1.auth_user_id
    
    # Create Channel_1 made by user_1 and get its id
    Channel_1 = channels_create_v1(user_1_id_auth, channelone, True)
    Channel_1_id = Channel_1.channel_id
    
    # Calls details function for testing
    channel_details_v1(user_1_id_auth, Channel_1_id)
    
    pass
    
# Case 2 - tests for valid function implementation with multiple group member
#          expected outcome is output of {name, owner_members, all_members}
# Occurs when channel is valid and there are multiple member in that group
def test_channel_details_v1_success():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    user_1 = auth_register_v1(user1@gmail.com, user1pass, numerouno, uno)
    user_2 = auth_register_v1(user2@gmail.com, user2pass, numerodos, dos)
    user_1 = auth_login_v1(user1@gmail.com, user1pass)
    user_2 = auth_login_v1(user2@gmail.com, user2pass)

    # Identify user_id and auth_user_id for 2 registered user for testing
    user_1_id = user_1.u_id
    user_2_id = user_2.u_id
    user_1_id_auth = user_1.auth_user_id
    
    # Create Channel_1 made by user_1 and get its id
    Channel_1 = channels_create_v1(user_1_id_auth, channelone, True)
    Channel_1_id = Channel_1.channel_id
    
    # Calls invite function 
    # (user 1 invites user 2 into the channel he/she is in)
    channel_invite_v1(user_1_id_auth, Channel_1_id, user_2_id)
    
    # Calls details function for testing
    channel_details_v1(user_1_id_auth, Channel_1_id)
    
    pass

# Case 3 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel_id does not refer to a valid channel.
def test_channel_details_v1_inputError():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    user_1 = auth_register_v1(user1@gmail.com, user1pass, numerouno, uno)
    user_2 = auth_register_v1(user2@gmail.com, user2pass, numerodos, dos)
    user_1 = auth_login_v1(user1@gmail.com, user1pass)
    user_2 = auth_login_v1(user2@gmail.com, user2pass)

    # Identify user_id and auth_user_id for 2 registered user for testing
    user_1_id = user_1.u_id
    user_2_id = user_2.u_id
    user_1_id_auth = user_1.auth_user_id
    
    # Create Channel_1 made by user_1 and get its id
    Channel_1 = channels_create_v1(user_1_id_auth, channelone, True)
    Channel_1_id = Channel_1.channel_id
    
    # Made an invalid channel id for testing
    Channel_1_invalidid = Channel_1_id + 300
    
    # Conditions leads to an input error outcome and tests for it
    with pytest.raises(InputError):
        channel_details_v1(user_1_id_auth, Channel_1_invalidid)

# Case 4 - tests for access error
#          expected outcome is access error
# Occurs when the authorised user is not a member of channel with channel_id
def test_channel_details_v1_accessError():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    user_1 = auth_register_v1(user1@gmail.com, user1pass, numerouno, uno)
    user_2 = auth_register_v1(user2@gmail.com, user2pass, numerodos, dos)
    user_1 = auth_login_v1(user1@gmail.com, user1pass)
    user_2 = auth_login_v1(user2@gmail.com, user2pass)

    # Identify user_id and auth_user_id for 2 registered user for testing
    user_1_id = user_1.u_id
    user_2_id = user_2.u_id
    user_1_id_auth = user_1.auth_user_id
    user_2_id_auth = user_2.auth_user_id
    
    # Create Channel_1 made by user_1 and get its id
    Channel_1 = channels_create_v1(user_1_id_auth, channelone, True)
    Channel_1_id = Channel_1.channel_id
    
    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channel_details_v1(user_2_id_auth, Channel_1_id)
