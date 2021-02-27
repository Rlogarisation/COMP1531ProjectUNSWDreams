# by Lan Lin

import pytest
import re
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError


# test email does not match the regular expression
def test_auth_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('123.com', '12345', 'Lan', 'Lin')
        auth_register_v1('abc@@@.com', '0823hds', 'Langley', 'Lin')


# test email address is already being used by another user
def test_auth_register_duplicate_email():
    clear_v1()
    auth_register_v1('haha1@gmail.com', 'shkdlch', 'Peter', 'White')
    with pytest.raises(InputError):
        auth_register_v1('haha1@gmail.com', '0w9edu', 'Tom', 'White')


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
        auth_register_v1('haha@gmail.com', '123', '', 'White')
        auth_register_v1('haha2@gmail.com', 'iwsd', name, 'White')


# name_last is not between 1 and 50 characters inclusively in length
def test_auth_register_lastName_length():
    clear_v1()
    name = 'a' * 51
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123', 'Peter', '')
        auth_register_v1('haha2@gmail.com', 'iwsd', 'Tom', name)








