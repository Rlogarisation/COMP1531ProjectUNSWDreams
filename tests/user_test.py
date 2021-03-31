import pytest
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, auth_logout, get_user_by_token
from src.error import InputError, AccessError
from src.channel import channel_details_v1, channel_invite_v1, channel_join_v1
from src.channels import channels_create_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1, \
    users_all, admin_user_remove, admin_userpermission_change
from src.data_file import Permission
"""
Author: Emir Aditya Zen

This file is for testing user_profile_v1 function implementation

Background
For a valid user, returns information about their user_id, email, first name,
last name, and handle

HTTP Method: GET

Parameters: (token, u_id)
Return Type: { user }

InputError:
- u_id does not refer to a valid user

AccessError:
- The function is called with an invalid token
"""
#############################################################################
#                                                                           #
#                        Test for user_profile_v1                           #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is function returns user details
# Occurs when user and token is valid
def test_user_profile_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']

    # Check output if correct
    assert user1['email'] == "haha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Peter"
    assert user1['name_last'] == "White"
    assert user1['handle_str'] == "peterwhite"


# Case 2 - tests for multiple valid function implementation (no errors expected)
#          expected outcome is function returns multiple users details
# Occurs when user and token is valid
def test_user_profile_v1_successMultiple():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    token2 = token_id_dict2["token"]
    u_id1 = token_id_dict1["auth_user_id"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']
    user2 = user_profile_v1(token2, u_id2)['user']

    # Check output if correct
    assert user1['email'] == "haha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Peter"
    assert user1['name_last'] == "White"
    assert user1['handle_str'] == "peterwhite"
    assert user2['email'] == "test@testexample.com"
    assert user2['u_id'] == u_id2
    assert user2['name_first'] == "Tom"
    assert user2['name_last'] == "Green"
    assert user2['handle_str'] == "tomgreen"


# Case 3 - tests for input error outcome
#          expected outcome is input error
# Occurs when user id is invalid
def test_user_profile_v1_inputError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Made an invalid user id for testing
    invalid_id = u_id1 + 300

    # Test conditions leading to an input error outcome due to invalid user_id
    with pytest.raises(InputError):
        user_profile_v1(token1, invalid_id)


# Case 4 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_user_profile_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        user_profile_v1(invalid_token, u_id1)


"""
Author: Emir Aditya Zen

This file is for testing user_profile_setname_v1 function implementation

Background
Update the authorised users first and last name

HTTP Method: PUT

Parameters: (token, name_first, name_last)
Return Type: {}

InputError:
- name_first is not between 1-50 characters inclusively in length
- name_last is not between 1-50 characters inclusively in length

AccessError:
- The function is called with an invalid token
"""
#############################################################################
#                                                                           #
#                    Test for user_profile_setname_v1                       #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is function changes user name and outputs nothing
# Occurs when token, name_first, and name_last is valid
def test_user_profile_setname_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the user_profile_setname_v1 function to change name
    user_profile_setname_v1(token1, "Mark", "Johnson")

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']

    # Check output if correct
    assert user1['email'] == "haha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Mark"
    assert user1['name_last'] == "Johnson"


# Case 2 - tests for input error due to name_first
#          expected outcome is input error
# Occurs when name_first is not between 1 and 50 characters inclusively in length
def test_user_profile_setname_v1_inputError_nameFirst_caseOne():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid first name
    with pytest.raises(InputError):
        user_profile_setname_v1(token1, "", "Johnson")


# Case 3 - tests for input error due to name_first
#          expected outcome is input error
# Occurs when name_first is not between 1 and 50 characters inclusively in length
def test_user_profile_setname_v1_inputError_nameFirst_caseTwo():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid first_name for testing
    invalid_first_name = 51*"a"

    # Test conditions leading to an input error outcome due to invalid first name
    with pytest.raises(InputError):
        user_profile_setname_v1(token1, invalid_first_name, "Johnson")


# Case 4 - tests for input error due to name_last
#          expected outcome is input error
# Occurs when name_last is not between 1 and 50 characters inclusively in length
def test_user_profile_setname_v1_inputError_nameLast_caseOne():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid last name
    with pytest.raises(InputError):
        user_profile_setname_v1(token1, "Mark", "")


# Case 5 - tests for input error due to name_last
#          expected outcome is input error
# Occurs when name_last is not between 1 and 50 characters inclusively in length
def test_user_profile_setname_v1_inputError_nameLast_caseTwo():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid last_name for testing
    invalid_last_name = 51*"a"

    # Test conditions leading to an input error outcome due to invalid last name
    with pytest.raises(InputError):
        user_profile_setname_v1(token1, "Mark", invalid_last_name)


# Case 6 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_user_profile_setname_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        user_profile_setname_v1(invalid_token, "Mark", "Johnson")


"""
Author: Emir Aditya Zen

This file is for testing user_profile_setemail_v1 function implementation

Background
Update the authorised users email address

HTTP Method: PUT

Parameters: (token, email)
Return Type: {}

InputError:
- email is invalid
- email is already used by another user

AccessError:
- The function is called with an invalid token
"""
#############################################################################
#                                                                           #
#                   Test for user_profile_setemail_v1                       #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is function changes user email and outputs nothing
# Occurs when token and email is valid
def test_user_profile_setemail_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the user_profile_setemail_v1 function to change email
    user_profile_setemail_v1(token1, "newhaha@gmail.com")

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']

    # Check output if correct
    assert user1['email'] == "newhaha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Peter"
    assert user1['name_last'] == "White"
    assert user1['handle_str'] == "peterwhite"


# Case 2 - tests for input error due to email
#          expected outcome is input error
# Occurs when email inputted has not been used but invalid
def test_user_profile_setemail_v1_inputError_email_caseOne():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid email
    with pytest.raises(InputError):
        user_profile_setemail_v1(token1, "")


# Case 3 - tests for input error due to email
#          expected outcome is input error
# Occurs when email inputted has not been used but invalid
def test_user_profile_setemail_v1_inputError_email_caseTwo():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid email
    with pytest.raises(InputError):
        user_profile_setemail_v1(token1, "blablaadgmaildotcom")


# Case 4 - tests for input error due to repeated email
#          expected outcome is input error
# Occurs when email is valid but is used by another user
def test_user_profile_setemail_v1_inputError_repeatedEmail():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to repeated email
    with pytest.raises(InputError):
        user_profile_setemail_v1(token1, "test@testexample.com")


# Case 5 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_user_profile_setemail_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        user_profile_setemail_v1(invalid_token, "newhaha@gmail.com")


"""
Author: Emir Aditya Zen

This file is for testing user_profile_sethandle_v1 function implementation

Background
Update the authorised users handle

HTTP Method: PUT

Parameters: (token, handle_str)
Return Type: {}

InputError:
- handle_str is not between 3 and 20 characters inclusive
- handle_str is already used by another user

AccessError:
- The function is called with an invalid token
"""
#############################################################################
#                                                                           #
#                   Test for user_profile_sethandle_v1                      #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected)
#          expected outcome is function changes user handle and outputs nothing
# Occurs when token and handle_str is valid
def test_user_profile_sethandle_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the user_profile_sethandle_v1 function to change handle
    user_profile_sethandle_v1(token1, "markjohnson")

    # Calls the user_profile_v1 function for testing
    user1 = user_profile_v1(token1, u_id1)['user']

    # Check output if correct
    assert user1['email'] == "haha@gmail.com"
    assert user1['u_id'] == u_id1
    assert user1['name_first'] == "Peter"
    assert user1['name_last'] == "White"
    assert user1['handle_str'] == "markjohnson"


# Case 2 - tests for input error due to handle
#          expected outcome is input error
# Occurs when handle_str is not between 3 and 20 characters inclusive
def test_user_profile_sethandle_v1_inputError_handle_caseOne():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to invalid handle
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token1, "")


# Case 3 - tests for input error due to handle
#          expected outcome is input error
# Occurs when handle_str is not between 3 and 20 characters inclusive
def test_user_profile_sethandle_v1_inputError_handle_caseTwo():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid handle for testing
    invalid_handle = 51*"a"

    # Test conditions leading to an input error outcome due to invalid handle
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token1, invalid_handle)


# Case 4 - tests for input error due to repeated handle
#          expected outcome is input error
# Occurs when handle_str is valid but is used by another user
def test_user_profile_sethandle_v1_inputError_repeatedHandle():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]

    # Test conditions leading to an input error outcome due to repeated handle
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token1, "tomgreen")


# Case 5 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_user_profile_sethandle_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        user_profile_sethandle_v1(invalid_token, "markjohnson")


"""
Author: Emir Aditya Zen

This file is for testing users_all_v1 function implementation

Background
Returns a list of all users and their associated details

HTTP Method: GET

Parameters: (token)
Return Type: { users }

AccessError:
- The function is called with an invalid token
"""
#############################################################################
#                                                                           #
#                          Test for users_all_v1                            #
#                                                                           #
#############################################################################


# Case 1 - tests for valid function implementation (no errors expected) single user case
#          expected outcome is function outputs users as a list of dictionaries
# Occurs when token is valid and only 1 user is currently registered
def test_users_all_v1_success():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]
    u_id1 = token_id_dict1["auth_user_id"]

    # Calls the users_all_v1 function for testing
    output = users_all(token1)['users']

    # Check output if correct
    assert output[0]['email'] == "haha@gmail.com"
    assert output[0]['u_id'] == u_id1
    assert output[0]['name_first'] == "Peter"
    assert output[0]['name_last'] == "White"
    assert output[0]['handle_str'] == "peterwhite"


# Case 2 - tests for valid function implementation (no errors expected) multiple user case
#          expected outcome is function outputs users as a list of dictionaries
# Occurs when token is valid and multiple users is currently registered
def test_users_all_v1_successMultiple():
    # Clears data and registers and logins user_1 and user_2
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")
    auth_register_v1("test@testexample.com", "wp01^#$dp1o23", "Tom", "Green")

    # login the two registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token_id_dict2 = auth_login_v1("test@testexample.com", "wp01^#$dp1o23")
    token1 = token_id_dict1["token"]
    token2 = token_id_dict2["token"]
    u_id1 = token_id_dict1["auth_user_id"]
    u_id2 = token_id_dict2["auth_user_id"]

    # Calls the users_all_v1 function for testing
    output = users_all(token1)['users']

    # Check output if correct
    assert output[0]['email'] == "haha@gmail.com"
    assert output[0]['u_id'] == u_id1
    assert output[0]['name_first'] == "Peter"
    assert output[0]['name_last'] == "White"
    assert output[0]['handle_str'] == "peterwhite"
    assert output[1]['email'] == "test@testexample.com"
    assert output[1]['u_id'] == u_id2
    assert output[1]['name_first'] == "Tom"
    assert output[1]['name_last'] == "Green"
    assert output[1]['handle_str'] == "tomgreen"


# Case 5 - tests for access error outcome
#          expected outcome is access error
# Occurs when token is invalid
def test_users_all_v1_accessError():
    # Clears data and registers and logins user_1
    clear_v1()
    auth_register_v1("haha@gmail.com", "123123123", "Peter", "White")

    # login the registered users
    token_id_dict1 = auth_login_v1("haha@gmail.com", "123123123")
    token1 = token_id_dict1["token"]

    # Made an invalid token for testing
    invalid_token = token1 + "rkbgesorgbv#$%"

    # Test conditions leading to an access error outcome due to invalid token
    with pytest.raises(AccessError):
        users_all(invalid_token)

#############################################################################
#                                                                           #
#                       Test for admin_user_permission_change               #
#                                                                           #
#############################################################################
"""
Author: Lan Lin
Background: Given a User by their user ID, set their permissions 
to new permissions described by permission_id
Input Error: 
1. u_id does not refer to a valid user
2. permission_id does not refer to a value permission
Access Error: The authorised user is not an owner
"""


def test_invalid_token():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token = register1['token']
    invalid_token = f"{token}123"
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    u_id2 = register2['auth_user_id']
    new_permission_id = Permission.global_owner
    with pytest.raises(AccessError):
        admin_userpermission_change(invalid_token, u_id2, new_permission_id)


def test_admin_change_permission_invalid_owner():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    register3 = auth_register_v1('haha1@gmail.com', '1231231231', 'Pete', 'Whit')
    token2 = register2['token']
    uid3 = register3['auth_user_id']
    with pytest.raises(AccessError):
        admin_userpermission_change(token2, uid3, Permission.global_owner)


def test_admin_change_permission_invalid_user():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid2 = register2['auth_user_id']
    invalid_uid = uid2 + 100
    with pytest.raises(InputError):
        admin_userpermission_change(token1, invalid_uid, Permission.global_owner)


def test_admin_change_permission_invalid_permission():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid2 = register2['auth_user_id']
    invalid_permission = 3
    with pytest.raises(InputError):
        admin_userpermission_change(token1, uid2, invalid_permission)


def test_admin_change_permission_owner():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid2 = register2['auth_user_id']
    token2 = register2['token']
    admin_userpermission_change(token1, uid2, Permission.global_owner)
    channel_id = channels_create_v1(token1, "My Channel", False)['channel_id']
    channel_join_v1(token2, channel_id)


def test_admin_change_permission_member():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid1 = register1['auth_user_id']
    uid2 = register2['auth_user_id']
    token2 = register2['token']
    admin_userpermission_change(token1, uid2, Permission.global_owner)
    admin_userpermission_change(token2, uid1, Permission.global_member)
    channel_id = channels_create_v1(token2, "My Channel", False)['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1(token1, channel_id)


#############################################################################
#                                                                           #
#                       Test for admin_user_remove                          #
#                                                                           #
#############################################################################
"""
Author: Lan Lin
Background: Given a User by their user ID, remove the user from the Dreams.
Input Error: 
1. u_id does not refer to a valid user
2. The user is currently the only owner
Access Error: The authorised user is not an owner
"""


def test_admin_user_remove_invalid_uid():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = register1['token']
    with pytest.raises(InputError):
        admin_user_remove(token1, None)
    with pytest.raises(InputError):
        admin_user_remove(token1, 'hehe')


def test_admin_user_remove_only_owner():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = register1['token']
    uid1 = register1['auth_user_id']
    with pytest.raises(InputError):
        admin_user_remove(token1, uid1)


def test_admin_user_remove_invalid_owner():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token2 = register2['token']
    uid2 = register2['auth_user_id']
    with pytest.raises(AccessError):
        admin_user_remove(token2, uid2)


def test_admin_user_remove_successfully():
    clear_v1()
    regiester1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = regiester1['token']
    token2 = register2['token']
    uid2 = register2['auth_user_id']
    user_profile2 = user_profile_v1(token2, uid2)
    assert user_profile2['user']['email'] == 'test@testexample.com'
    admin_user_remove(token1, uid2)
    user_profile2 = user_profile_v1(token2, uid2)
    assert user_profile2['user']['name_first'] == 'Removed user'
    assert user_profile2['user']['name_last'] == 'Removed user'
