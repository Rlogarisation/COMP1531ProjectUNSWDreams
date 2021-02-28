# by Lan Lin

import pytest
import numpy
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, get_class_user
from src.error import InputError

"""
tests for auth_register_v1
"""


# test email does not match the regular expression
def test_auth_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('123.com', '12345ufd', 'Lan', 'Lin')
        auth_register_v1('abc@@@.com', '0823hdskhji', 'Langley', 'Lin')


# test email address is already being used by another user
def test_auth_register_duplicate_email():
    clear_v1()
    auth_register_v1('haha1@gmail.com', 'shkdlch', 'Peter', 'White')
    with pytest.raises(InputError):
        auth_register_v1('haha1@gmail.com', '0w9epodu', 'Tom', 'White')


# test for password entered is less than 6 characters long
def test_auth_register_pwd_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123', 'Tom', 'White')
        auth_register_v1('haha2@gmail.com', 'ab#', 'Peter', 'White')


# name_first is not between 1 and 50 characters inclusively in length
def test_auth_register_firstName_length():
    clear_v1()
    name = 'a' * 51
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123iwuiused', '', 'White')
        auth_register_v1('haha2@gmail.com', 'iwsdrjcio', name, 'White')


# name_last is not between 1 and 50 characters inclusively in length
def test_auth_register_lastName_length():
    clear_v1()
    name = 'a' * 51
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123kjsldfiew', 'Peter', '')
        auth_register_v1('haha2@gmail.com', 'iwsdcio3', 'Tom', name)


# test several users can successfully register
def test_auth_register_valid_small():
    clear_v1()
    # register a user with valid inputs
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')

    # test a dictionary is return
    assert isinstance(register1, dict)
    assert isinstance(register2, dict)

    # test the returned auth_user_id is not None
    assert len(register1) != 0
    assert len(register2) != 0

    # test the auth_user_id for different users are different
    auth_user_id1 = register1['auth_user_id']
    auth_user_id2 = register2['auth_user_id']
    assert auth_user_id1 != auth_user_id2


# test large number of users can register successfully
def test_auth_register_valid_large():
    clear_v1()
    id_list = []
    for index in range(50):
        person = auth_register_v1('example'+str(index)+'@testexample.com', 'abcuief98dh', 'Tom', 'Green')
        id_list[index] = person['auth_user_id']

    # check all auth_user_ids are unique
    # check the number of registered users are correct
    assert numpy.unique(id_list).size == len(id_list) == 50


# test if a valid handle is generated
def test_auth_register_handle_valid():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#123', 'Tommmmmmiweljnsyuoeqiof', 'Green')
    register3 = auth_register_v1('haha2@gmail.com', '123jcqewp2', 'Peter', 'White')

    auth_user_id1 = register1['auth_user_id']
    auth_user_id2 = register2['auth_user_id']
    auth_user_id3 = register3['auth_user_id']

    user1 = get_class_user(auth_user_id1)
    user2 = get_class_user(auth_user_id2)
    user3 = get_class_user(auth_user_id3)

    """
    - test if the handle is already taken, append the concatenated names with 
    the smallest number (starting at 0) that 
    forms a new handle that isn't already taken.
    - test if the concatenation is longer than 20 characters, it is cutoff at 20 characters.
    """

    assert user1.handle_str == 'peterwhite'
    assert user3.handle_str == 'paterwhite0'
    assert user2.handle_str == 'tommmmmmiweljnsgreen'


"""
tests for auth_login_v1
"""



