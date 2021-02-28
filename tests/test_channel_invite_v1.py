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

# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is user gets invited to a channel and gets added to it
# Occurs when channel is valid and user is valid whilst having not been invited before
def test_channel_invite_v1_success():
    

# Case 2 - tests for repeated invite instances
#          expected outcome is recognizes user invited is already in the channel and does nothing
# Occurs when channel is valid and user is already inside the channel
def test_channel_invite_v1_repeated():


# Case 3 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel_id does not refer to a valid channel.
def test_channel_invite_v1_inputErrorChannel():


# Case 4 - tests for input error due to invalid user
#          expected outcome is input error
# Occurs when u_id does not refer to a valid user.
def test_channel_invite_v1_inputErrorUser():


# Case 5 - tests for access error
#          expected outcome is access error
# Occurs when the authorised user is not already a member of the channel
def test_channel_invite_v1_accessError():
