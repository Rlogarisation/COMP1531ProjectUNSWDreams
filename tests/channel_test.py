# Imports the necessary function implementations
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, \
    channel_messages_v1, channel_join_v1
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1

# Imports the possible error output
from src.error import InputError, AccessError

# Imports current global listed data
from src.data_file import data, User, Channel

# Imports pytest
import pytest

"""
Author : Emir Aditya Zen

This file is for testing channel_invite_v1 function implementation

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

# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is user gets invited to a channel and gets added to it
# Occurs when channel is valid and user is valid whilst having not been invited before
def test_channel_invite_v1_success():
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
    
    # Calls invite function for testing 
    # (user 1 invites user 2 into the channel he/she is in)
    channel_invite_v1(user_1_id_auth, Channel_1_id, user_2_id)
    
    # Expected output is user_2 joins the Channel_1
    
    # Hence checks that Channel_1 exists, has 2 members, and the members are
    # user_1 and user_2
    num_members = 0
    for channel in data['class_channels']:
        if channel.channel_id == Channel_1_id:
            num_members = len(channel.all_members)
            break
    assert channel.all_members[0].u_id == user_1_id
    assert channel.all_members[1].u_id == user_2_id
    assert num_members == 2

# Case 2 - tests for repeated invite instances
#          expected outcome is recognizes user invited is already in the channel and does nothing
# Occurs when channel is valid and user is already inside the channel
def test_channel_invite_v1_repeated():
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
    
    # Calls invite function twice targeting the same user for testing repetition
    # (user 1 invites user 2 into the channel he/she is in twice)
    channel_invite_v1(user_1_id_auth, Channel_1_id, user_2_id)
    channel_invite_v1(user_1_id_auth, Channel_1_id, user_2_id)
    
    # Expected output is user_2 joins the Channel_1 on the first invite and 
    # ignores the second invite
    
    # Hence checks that Channel_1 exists, has 2 members, and the members are
    # user_1 and user_2
    num_members = 0
    for channel in data['class_channels']:
        if channel.channel_id == Channel_1_id:
            num_members = len(channel.all_members)
            break
    assert channel.all_members[0].u_id == user_1_id
    assert channel.all_members[1].u_id == user_2_id
    assert num_members == 2

# Case 3 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel_id does not refer to a valid channel.
def test_channel_invite_v1_inputErrorChannel():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    user_1 = auth_register_v1(user1@gmail.com, user1pass, numerouno, uno)
    user_2 = auth_register_v1(user2@gmail.com, user2pass, numerodos, dos)
    user_1 = auth_login_v1(user1@gmail.com, user1pass)
    user_2 = auth_login_v1(user2@gmail.com, user2pass)

    # Identify user id for 2 registered user for testing
    user_1_id = user_1.u_id
    user_2_id = user_2.u_id
    user_1_id_auth = user_1.auth_user_id
    
    # Create Channel_1 made by user_1 and get its id
    Channel_1 = channels_create_v1(user_1_id_auth, channelone, True)
    Channel_1_id = Channel_1.channel_id
    
    # Made an invalid channel id for testing
    Channel_1_invalid_id = Channel_1_id + 300
    
    # Test conditions leading to an input error outcome due to invalid channel_id
    with pytest.raises(InputError):
        channel_invite(user_1_id_auth, Channel_1_invalid_id, user_2_id)
    

# Case 4 - tests for input error due to invalid user
#          expected outcome is input error
# Occurs when u_id does not refer to a valid user.
def test_channel_invite_v1_inputErrorUser():
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
    
    # Made an invalid user id for user 2
    user_2_id_invalid_id = user_2_id + 300
    
    # Test conditions leading to an input error outcome due to invalid u_id
    with pytest.raises(InputError):
        channel_invite(user_1_id_auth, Channel_1_id, user_2_id_invalid_id)

# Case 5 - tests for access error
#          expected outcome is access error
# Occurs when the authorised user is not already a member of the channel
# Meaning user 2 invites user 3 into a channel eventhough channel was made by user 1
def test_channel_invite_v1_accessError():
    # Clears data and registers and logins user_1, user_2, and user_3
    clear_v1()
    user_1 = auth_register_v1(user1@gmail.com, user1pass, numerouno, uno)
    user_2 = auth_register_v1(user2@gmail.com, user2pass, numerodos, dos)
    user_3 = auth_register_v1(user3@gmail.com, user3pass, numerotres, tres)
    user_1 = auth_login_v1(user1@gmail.com, user1pass)
    user_2 = auth_login_v1(user2@gmail.com, user2pass)
    user_3 = auth_login_v1(user3@gmail.com, user3pass)

    # Identify user_id and auth_user_id for 3 registered user for testing
    user_1_id = user_1.u_id
    user_2_id = user_2.u_id
    user_3_id = user_3.u_id
    user_1_id_auth = user_1.auth_user_id
    user_2_id_auth = user_2.auth_user_id
    
    # Create Channel_1 made by user_1 and get its id
    Channel_1 = channels_create_v1(user_1_id_auth, channelone, True)
    Channel_1_id = Channel_1.channel_id
    
    # Test conditions leading to an access error outcome
    with pytest.raises(AccessError):
        channel_invite(user_2_id_auth, Channel_1_id, user_3_id)

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
    
"""

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
    output = channel_details_v1(user_1_id_auth, Channel_1_id)
    
    assert output['all_members'][0].u_id == user_1_id
    assert output['owner_members'][0].u_id == user_1_id
    assert output['name'] == 'channelone'
    
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
    
    assert output['all_members'][0].u_id == user_1_id
    assert output['all_members'][1].u_id == user_2_id
    assert output['owner_members'][0].u_id == user_1_id
    assert output['name'] == 'channelone'

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