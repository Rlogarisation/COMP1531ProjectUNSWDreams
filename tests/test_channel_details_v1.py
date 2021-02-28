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
#          expected outcome is output of {name, owner_members, all_members}
# Occurs when channel is valid
def test_channel_details_v1_success():


# Case 2 - tests for input error due to invalid channel
#          expected outcome is input error
# Occurs when channel_id does not refer to a valid channel.
def test_channel_details_v1_inputErrorChannel():


# Case 3 - tests for access error
#          expected outcome is access error
# Occurs when the authorised user is not a member of channel with channel_id
def test_channel_details_v1_accessError():

