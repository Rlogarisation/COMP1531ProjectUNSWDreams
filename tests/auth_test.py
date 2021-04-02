import pytest
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v2, auth_logout, get_user_by_token
from src.error import InputError, AccessError
from src.channel import channel_details_v1, channel_invite_v1
from src.channels import channels_create_v1

"""
Author: Lan Lin

Test for auth_register_v2 function implementation

Tests content:
1. The email is invalid
2. The email address is already been used by another user
3. Password length is less than 6 characters
4. The length of name_first is not between 1 and 50
5. The length of name_last is not between 1 and 50
6. Successfully register several users
7. Successfully register large amount users
8. Test if the handle generated is valid
"""
#############################################################################
#                                                                           #
#                       Test for auth_register_v2                           #
#                                                                           #
#############################################################################


# test email does not match the regular expression
def test_auth_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('123.com', '12345ufd', 'Lan', 'Lin')
        auth_register_v2('abc@@@.com', '0823hdskhji', 'Langley', 'Lin')


# test email address is already being used by another user
def test_auth_register_duplicate_email():
    clear_v1()
    auth_register_v2('haha1@gmail.com', 'shkdlch', 'Peter', 'White')
    with pytest.raises(InputError):
        auth_register_v2('haha1@gmail.com', '0w9epodu', 'Tom', 'White')


# test for password entered is less than 6 characters long
def test_auth_register_pwd_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('haha@gmail.com', '123', 'Tom', 'White')
        auth_register_v2('haha2@gmail.com', 'ab#', 'Peter', 'White')


# name_first is not between 1 and 50 characters inclusively in length
def test_auth_register_firstName_length():
    clear_v1()
    name = 'a' * 51
    with pytest.raises(InputError):
        auth_register_v2('haha@gmail.com', '123iwuiused', '', 'White')
        auth_register_v2('haha2@gmail.com', 'iwsdrjcio', name, 'White')


# name_last is not between 1 and 50 characters inclusively in length
def test_auth_register_lastName_length():
    clear_v1()
    name = 'a' * 51
    with pytest.raises(InputError):
        auth_register_v2('haha@gmail.com', '123kjsldfiew', 'Peter', '')
        auth_register_v2('haha2@gmail.com', 'iwsdcio3', 'Tom', name)


# test several users can successfully register
def test_auth_register_valid_small():
    clear_v1()
    # register two users with valid inputs
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')

    # test a dictionary is return
    assert isinstance(register1, dict)
    assert isinstance(register2, dict)

    # test the returned auth_user_id is not None
    assert len(register1) != 0
    assert len(register2) != 0

    # test the auth_user_id for different users are different
    auth_user_id1 = register1['auth_user_id']
    auth_user_id2 = register2['auth_user_id']
    token1 = register1['token']
    token2 = register2['token']
    assert auth_user_id1 != auth_user_id2
    assert token1 != token2


# test large number of users can register successfully
def test_auth_register_valid_large():
    clear_v1()
    id_list = []
    for index in range(50):
        person = auth_register_v2('example'+str(index)+'@testexample.com', 'abcuief98dh', 'Tom', 'Green')
        # check the auth_user_id generated is correct
        assert person['auth_user_id'] == index
        id_list.append(person['auth_user_id'])

    # check all auth_user_ids are unique
    # check the number of registered users are correct
    assert len(set(id_list)) == len(id_list) == 50


# test if a valid handle is generated
def test_auth_register_handle_valid():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'zxcvbnmasdfg', 'hjklqwe')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#123', 'zxcvbnmasdfg', 'hjklqwert')
    register3 = auth_register_v2('haha2@gmail.com', '123jcqewp2', 'zxcvbnmasdfg', 'hjklqwert')
    register4 = auth_register_v2('haha3@gmail.com', '123jcqewp2', 'zxcvbnmasdfg', 'hjklqwertiowjec')

    token1 = register1['token']
    user_id2 = register2['auth_user_id']
    user_id3 = register3['auth_user_id']
    user_id4 = register4['auth_user_id']

    channel_id = channels_create_v1(token1, 'Zoom', True)['channel_id']
    channel_invite_v1(token1, channel_id, user_id2)
    channel_invite_v1(token1, channel_id, user_id3)
    channel_invite_v1(token1, channel_id, user_id4)
    channel_members = channel_details_v1(token1, channel_id)['all_members']
    member1 = channel_members[0]
    member2 = channel_members[1]
    member3 = channel_members[2]
    member4 = channel_members[3]

    """
    - test if the handle is already taken, append the concatenated names with 
    the smallest number (starting at 0) that 
    forms a new handle that isn't already taken.
    - test if the concatenation is longer than 20 characters, it is cutoff at 20 characters.
    """

    assert member1['handle_str'] == 'zxcvbnmasdfghjklqwe'
    assert member2['handle_str'] == 'zxcvbnmasdfghjklqwer'
    assert member3['handle_str'] == 'zxcvbnmasdfghjklqwe0'
    assert member4['handle_str'] == 'zxcvbnmasdfghjklqwe1'


"""
Author : Lan Lin

Test for auth_login_v1 function implementation

Tests content:
1. The email is invalid
2. The email address does not belong to any user
3. Password is wrong
4. The users can successfully register
"""
#############################################################################
#                                                                           #
#                       Test for auth_login_v1                           #
#                                                                           #
#############################################################################


# test for email entered is not a valid email
def test_auth_login_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('123.@com', '12345ufd')
        auth_login_v1('a.,#0@test.com', '0823hdskhji')


# test for email entered does not belong to a user
def test_auth_login_not_registered_email():
    clear_v1()
    # register a user
    auth_register_v2('haha@gmail.com', '123123123', 'Tom', 'Green')
    # login the user with not registered email
    # will give error
    with pytest.raises(InputError):
        auth_login_v1('haha2@gmail.com', '123123123')


# test for password is not correct
def test_auth_login_wrong_password():
    clear_v1()
    auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'Green')
    with pytest.raises(InputError):
        auth_login_v1('haha@gmail.com', 'jfqowei0-23opj')


# test for users can login successfully
def test_auth_login_valid():
    clear_v1()
    # register two users with valid inputs
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')

    # login the two registered users
    login1 = auth_login_v1('haha@gmail.com', '123123123')
    login2 = auth_login_v1('test@testexample.com', 'wp01^#$dp1o23')

    # test the auth_user_id returned by login is the same with register
    # test the auth_user_id generated is correct
    assert register1['auth_user_id'] == login1['auth_user_id']
    assert register2['auth_user_id'] == login2['auth_user_id']
    # test that tokens are different
    assert login1['token'] != register1['token']
    assert login2['token'] != register2['token']


# test for the same user with different sessions
def test_auth_login_different_sessions():
    clear_v1()
    auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')

    login1 = auth_login_v1('haha@gmail.com', '123123123')
    login2 = auth_login_v1('haha@gmail.com', '123123123')
    login3 = auth_login_v1('haha@gmail.com', '123123123')
    auth_user_id1 = login1['auth_user_id']
    auth_user_id2 = login2['auth_user_id']
    auth_user_id3 = login3['auth_user_id']
    token1 = login1['token']
    token2 = login2['token']
    token3 = login3['token']
    assert auth_user_id1 == auth_user_id2 == auth_user_id3
    assert token1 != token2 != token3
#############################################################################
#                                                                           #
#                       Test for auth_logout                                #
#                                                                           #
#############################################################################


def test_auth_logout_invalid_token():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    token = register1['token']
    invalid_token = f"{token}123"
    assert auth_logout(invalid_token) == {'is_success': False}


def test_auth_logout_successfully_small():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = register1['token']
    # user1 = get_user_by_token(token1)
    login2 = auth_login_v1('haha@gmail.com', '123123123')
    # assert len(user1.current_sessions) == 2
    token2 = login2['token']
    assert auth_logout(token1) == {'is_success': True}
    # assert len(user1.current_sessions) == 1
    assert auth_logout(token2) == {'is_success': True}
    # assert len(user1.current_sessions) == 0


def test_auth_logout_successfully_large():
    clear_v1()
    auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    token_list = []
    for _i in range(20):
        login = auth_login_v1(f'haha@gmail.com', '123123123')
        token_list.append(login['token'])
    for token in token_list:
        result = auth_logout(token)
        assert result == {'is_success': True}


