import pytest
from src.channel import channel_invite_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.other import clear_v1
from src.auth import auth_register_v1


def test_clear_v1():
    #clear all of information to run test
    clear_v1()

    #create an user with details to run test
    register = auth_register_v1('user@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    user_id = register['auth_user_id']
    #create a channel 
    channel1_id = channels_create_v1(user_id, 'test_channel', True)['channel_id']
    #check if the user and channel are created correctly 
    channel_invite_v1(user_id, channel1_id, user_id)
    assert channels_list_v1(user_id) == ['test_channel']
    assert channels_listall_v1(user_id) == ['test-channel']
    
    
    #clear the information we created and check the validity of clear_v1
    clear_v1()
    assert channels_listall_v1(user_id) == []
