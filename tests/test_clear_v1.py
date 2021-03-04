import pytest
from src.data_file import data
from src.channels import channels_create_v1
from src.other import clear_v1
from src.auth import auth_register_v1


def test_clear_v1():
    #clear all of information to run test
    clear_v1()

    #create an user with details to run test
    register = auth_register_v1('user@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    user_id = register['auth_user_id']
    #create a channel 
    channel_id = channels_create_v1(user_id, 'test_channel', True)['channel_id']
    #check if the user and channel are created correctly in the empty dict
    assert data['class_channels'][0].name == 'test_channel'
    assert data['class_channels'][0].channel_id == channel_id 
    assert data['class_channels'][0].is_public == True
    assert data['class_user'][0].u_id == user_id
    assert data['class_user'][0].email == 'user@gmail.com'
    assert data['class_user'][0].name_first == 'shaozhen'
    assert data['class_user'][0].name_last == 'yan'
    
    #clear the information we created and check the validity of clear_v1
    clear_v1()
    assert data['class_channels'] == []
    assert data['class_user'] == []
    
    
    