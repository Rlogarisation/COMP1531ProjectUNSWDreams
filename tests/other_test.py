import pytest
import pickle

from src.channel import channel_invite_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.other import clear_v1
from src.auth import auth_register_v2
"""
Author : Shaozhen Yan

This file is for testing clear_v1 function implementation

Background
Resets the internal data of the application to it's initial state

Parameters: ()
Return Type: {}
"""


def test_clear_v1():
    # clear all of information to run test
    clear_v1()

    # create an user with details to run test
    register = auth_register_v2('user@gmail.com', 'qwe1212', 'shaozhen', 'yan')

    # create channels
    channel0_id = channels_create_v1(register['token'], 'test_public_channel', True)['channel_id']
    channel1_id = channels_create_v1(register['token'], 'test_private_channel', False)['channel_id']

    # check if the user and channel are created correctly
    assert channels_listall_v1(register['token'])['channels'][0] == {'channel_id': 0, 'name': 'test_public_channel'}
    assert channels_listall_v1(register['token'])['channels'][1] == {'channel_id': 1, 'name': 'test_private_channel'}

    # clear the information we created and check the validity of clear_v1
    clear_v1()
    # FIXME: 这边check clear validity为什么check register的？register不应该清楚数据了么？
    assert register['auth_user_id'] == 0
    register = auth_register_v2('user@gmail.com', 'qwe1212', 'shaozhen', 'yan')

    assert channels_listall_v1(register['token'])['channels'] == []


# def write_in_sth():
#     # create an user with details to run test
#     register = auth_register_v2('user@gmail.com', 'qwe1212', 'shaozhen', 'yan')

#     # create channels
#     channel0_id = channels_create_v1(register['token'], 'test_public_channel', True)['channel_id']
#     channel1_id = channels_create_v1(register['token'], 'test_private_channel', False)['channel_id']

#     # check if the user and channel are created correctly
#     assert channels_listall_v1(register['token'])['channels'][0] == {'channel_id': 0, 'name': 'test_public_channel'}
#     assert channels_listall_v1(register['token'])['channels'][1] == {'channel_id': 1, 'name': 'test_private_channel'}

# def print_db_file():
#     f1 = open('db.p', 'rb')
#     contents = pickle.load(f1)

#     print(contents)

# if __name__ == "__main__":
#     print_db_file()
#     write_in_sth()
#     print_db_file()
