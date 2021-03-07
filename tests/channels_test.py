# channels_test.py is used to test the file called channels 
# for 21T1 COMP1531 project
# Written by Zheng Luo (z5206267@ad.unsw.edu.au) on 28/Feb/2021


import pytest
from src.auth import auth_login_v1, auth_register_v1, create_role
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1, channel_messages_v1
from src.channels import channels_list_v1, channels_create_v1, channels_listall_v1
from src.error import InputError
from src.other import clear_v1

#############################################################################
#                                                                           #
#                       Test for channels_list_v1                           #
#                                                                           #
#############################################################################
"""
channels_list():

Provide a list of all channels (both public and private channels).

Parameters:(auth_user_id)
Return Type:{channels}

TEST CASES:
	-check the correctness of channel that the authorised user is belonged to.
	-check the detail and amount of channels for return

"""


def test_channels_correct_channel():
	clear_v1()
	# Initiate a user
	register1 = auth_register_v1("ZhengRogerLuo@gmail.com", "happysheepQAQ", "Zheng", "Luo")
	auth_user_id1 = register1['auth_user_id']
	user1 = auth_user_id1
	
	# Create a channel
	# channels_create_v1(auth_user_id, name, is_public)
	channel_id1 = channels_create_v1(auth_user_id1, "SheepChannel", is_public=True)['channel_id']

	# List the channel of this user belongs to
	channel_list = channels_list_v1(auth_user_id1)
	# Check the information of authorised user is correct
	assert (channel_list[0]['name'] == 'SheepChannel')


def test_channels_multiple_channels():
	clear_v1()
	# Initiate a user
	register1 = auth_register_v1("UNSWIsTheBest@gmail.com", "happyEveryday!", "Ian", "J")
	auth_user_id1 = register1['auth_user_id']
	user1 = auth_user_id1
	# Create multiple channels
	channel_id1 = channels_create_v1(auth_user_id1, "EngineeringChannel", is_public=True)['channel_id']
	channel_id2 = channels_create_v1(auth_user_id1, "BussinessChannel", is_public=True)['channel_id']
	channel_id3 = channels_create_v1(auth_user_id1, "LawChannel", is_public=True)['channel_id']

	# List the channel of this user belongs to
	channel_list = channels_list_v1(auth_user_id1)
	# Check the information of authorised user is correct
	assert (channel_list[0]['name'] == "EngineeringChannel")
	assert (channel_list[1]['name'] == "BussinessChannel")
	assert (channel_list[2]['name'] == "LawChannel")


def test_channels_multiple_users():
	clear_v1()
	# Initiate multiple users
	register1 = auth_register_v1("ILoveTrimester@gmail.com", "NoStressAtAll", "Iannnn", "J")
	register2 = auth_register_v1("IHateSemester@gmail.com", "BreakIsTooLong", "Ben", "A")
	auth_user_id1 = register1['auth_user_id']
	user1 = auth_user_id1
	auth_user_id2 = register2['auth_user_id']
	user2 = auth_user_id2
	# Create a channel
	channel_id1 = channels_create_v1(auth_user_id1, "mesterChannel", is_public=True)['channel_id']
	# Obtain the u_id of user,
	# so we can obtain the u_id for next step.
	# first input in inviter, third input is invitee.
	channel_invite_v1(auth_user_id1, channel_id1, user2)

	# channel_invite_v1(auth_user_id1, channel_id1, channel_detail2['owner_members'][0]['u_id'])
	# List the channel of first user belongs to
	channel_user1 = channels_list_v1(auth_user_id1)
	# List the channel of second user belongs to
	channel_user2 = channels_list_v1(auth_user_id2)
	# Check the information of authorised user is correct
	assert (channel_user1[0]['name'] == "mesterChannel")
	assert (channel_user2[0]['name'] == "mesterChannel")


def test_channels_oneUser_multiple_private_channels():
	clear_v1()
	# Initiate a user
	register1 = auth_register_v1("ILoveTrimester@gmail.com", "NoStressAtAll", "Iannnn", "J")
	auth_user_id1 = register1['auth_user_id']
	user1 = auth_user_id1
	# Create 2 private channels and 2 public channels
	channel_id1 = channels_create_v1(auth_user_id1, "ChannelAPublic", is_public=True)['channel_id']
	channel_id2 = channels_create_v1(auth_user_id1, "ChannelBPublic", is_public=True)['channel_id']
	channel_id3 = channels_create_v1(auth_user_id1, "ChannelCPrivate", is_public=False)['channel_id']
	channel_id4 = channels_create_v1(auth_user_id1, "ChannelDPrivate", is_public=False)['channel_id']
	# List all the public channel of the user belongs to
	channel_user1 = channels_list_v1(auth_user_id1)
	# Check the information of authorised user is correct
	assert len(channel_user1) == 4


#############################################################################
#                                                                           #
#                       Test for channels_listall_v1                        #
#                                                                           #
#############################################################################
"""
channels_listall_v1:

Provide a list of all channels (and their associated details)
Explaination:
channel_listall_v1 should list all channels, 
including those that are private, regardless of who calls it.

Parameters:(auth_user_id)
Return Type:{channels}

TEST CASES:
	-check the correctness of channel that the authorised user is belonged to.
	-check the detail and amount of channels for return

"""


def test_allchannels_correct_channel():
	clear_v1()
	# Initiate a user
	register1 = auth_register_v1("ZhengRogerLuo@gmail.com", "happysheepQAQ", "Zheng", "Luo")
	auth_user_id1 = register1['auth_user_id']
	user1 = auth_user_id1
	# Create a channel
	# channels_create_v1(auth_user_id, name, is_public)
	channel_id1 = channels_create_v1(auth_user_id1, "SheepChannel", is_public=True)['channel_id']
	# List amount of channels
	assert(len(channels_listall_v1(auth_user_id1)) == 1)


def test_allchannels_multiple_channels():
	clear_v1()
	# Initiate a user
	register1 = auth_register_v1("UNSWIsTheBest@gmail.com", "happyEveryday!", "Ian", "J")
	auth_user_id1 = register1['auth_user_id']
	user1 = auth_user_id1
	# Create multiple channels
	channel_id1 = channels_create_v1(auth_user_id1, "EngineeringChannel", is_public=True)['channel_id']
	channel_id2 = channels_create_v1(auth_user_id1, "BussinessChannel", is_public=True)['channel_id']
	channel_id3 = channels_create_v1(auth_user_id1, "LawChannel", is_public=True)['channel_id']
	# List amount of channels
	assert(len(channels_listall_v1(auth_user_id1)) == 3)


def test_allchannels_multiple_users():
	clear_v1()
	# Initiate multiple users
	register1 = auth_register_v1("ILoveTrimester@gmail.com", "NoStressAtAll", "Iannnn", "J")
	register2 = auth_register_v1("IHateSemester@gmail.com", "BreakIsTooLong", "Ben", "A")
	auth_user_id1 = register1['auth_user_id']
	user1 = auth_user_id1
	auth_user_id2 = register2['auth_user_id']
	user2 = auth_user_id2
	# Create two channels
	channel_id1 = channels_create_v1(auth_user_id1, "mesterChannel", is_public=True)['channel_id']
	channel_id2 = channels_create_v1(auth_user_id1, "mesterChannel2", is_public=True)['channel_id']
	# List amount of channels
	assert(len(channels_listall_v1(auth_user_id2)) == 2)


def test_allchannels_private():
	clear_v1()
	# Initiate a user
	register1 = auth_register_v1("UNSWIsTheBest@gmail.com", "happyEveryday!", "Ian", "J")
	auth_user_id1 = register1['auth_user_id']
	user1 = auth_user_id1
	# Create multiple channels
	# First channel is public, but all others are private,
	# listall function able to check all of these.
	channel_id1 = channels_create_v1(auth_user_id1, "EngineeringChannel", is_public=True)['channel_id']
	channel_id2 = channels_create_v1(auth_user_id1, "BussinessChannel", is_public=False)['channel_id']
	channel_id3 = channels_create_v1(auth_user_id1, "LawChannel", is_public=False)['channel_id']
	# List amount of channels
	assert(len(channels_listall_v1(auth_user_id1)) == 3)

#############################################################################
#                                                                           #
#                        Test for channels_create_v1                        #
#                                                                           #
#############################################################################

# test if the name of the channel to be created is less than 20 characters
def test_channels_create_length_of_name():
	clear_v1()
	register = auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
	auth_user_id = register['auth_user_id']
	# check the length of name is more than 20 characters
	with pytest.raises(InputError):
		channels_create_v1(auth_user_id, 'A name clearly more than 20 characters', True)


# check the is_public is boolean or not
def test_channels_create_is_public_bool():
	clear_v1()
	register = auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
	auth_user_id = register['auth_user_id']
	with pytest.raises(InputError):
		channels_create_v1(auth_user_id, 'good_channel', 'not_a_bool')


# test if the channel has been created successfully
def test_channels_create_valid():
	clear_v1()
	auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
	login = auth_login_v1('haha@gmail.com', '123123123')
	auth_user_id = login['auth_user_id']

	channel1_id = channels_create_v1(auth_user_id, "public_channel", True)['channel_id']
	channel2_id = channels_create_v1(auth_user_id, "private_channel", False)['channel_id']

	channel_detail1 = channel_details_v1(auth_user_id, channel1_id)
	channel_detail2 = channel_details_v1(auth_user_id, channel2_id)
	assert channel_detail1['name'] == 'public_channel'
	assert channel_detail2['name'] == 'private_channel'
	owner1 = channel_detail1['owner_members'][0]
	member1 = channel_detail1['all_members'][0]
	owner2 = channel_detail1['owner_members'][0]
	member2 = channel_detail1['all_members'][0]
	assert owner1['email'] == owner2['email'] == member1['email'] == member2['email'] == 'haha@gmail.com'
	assert len(channels_list_v1(auth_user_id)) == 2
