import re
import jwt
import hashlib
import random
import smtplib

from jwt import InvalidSignatureError, InvalidTokenError
from src.data_file import User, Permission, data
from src.error import InputError

#############################################################################
#                                                                           #
#                           Interface function                              #
#                                                                           #
#############################################################################
"""
Author: Lan Lin

Background
Given a user's first and last name, email address, and password,
create a new account for them and return a new `auth_user_id`

Parameters: email, password, name_first, name_last
Return Type: { auth_user_id }

InputError:
- Email is not valid
- Email address is used by another user
- Password is less than 6 characters
- The length of name_first is not between 1 and 50
- The length of name_last is not between 1 and 50
"""


def auth_register_v1(email, password, name_first, name_last):
    auth_register_check_error(email, password, name_first, name_last)

    u_id = create_uid()
    auth_user_id = create_auth_user_id(u_id)
    handle = create_handle(name_first, name_last)
    permission_id = create_permission(u_id)
    hashed_password = hash_password(password)

    user_ = User(u_id, email, hashed_password, name_first, name_last, handle, auth_user_id, permission_id)
    session_id = create_session_id()
    token = session_to_token(session_id)
    user_.current_sessions.append(session_id)

    data['class_users'].append(user_)

    return {
        'token': token,
        'auth_user_id': auth_user_id
    }


"""
Author : Lan Lin

Background
Given a registered users' email and password and returns their `auth_user_id` value

Parameters: email, password
Return Type: { auth_user_id }

InputError:
- Email is not valid
- Email address does not belong to any user
- Password is wrong
"""


def auth_login_v1(email, password):
    auth_login_error_check(email, password)

    user = get_user_by_email(email)
    session_id = create_session_id()
    user.current_sessions.append(session_id)
    token = session_to_token(session_id)
    return {
        'token': token,
        'auth_user_id': user.auth_user_id
    }


def auth_logout(token):
    user_session = get_user_session_by_token(token)
    if user_session is not None:
        user = user_session[0]
        session_id = user_session[1]
        user.current_sessions.remove(session_id)
        return {'is_success': True}

    return {'is_success': False}


def auth_passwordreset_request_v1(email):
    user = get_user_by_email(email)
    if user is None:
        raise InputError(description="The email is invalid")

    # generate the reset code
    reset_code = create_reset_code()
    user.reset_code = reset_code

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user='cblinker17@gmail.com', password='cs1531f11cblinker')
    connection.sendmail(
        from_addr='cblinker17@gmail.com',
        to_addrs=email,
        msg=f"Subject:Password Reset Code for Dreams\n\nThe password rest code is {reset_code}"
    )

    return {}


def auth_passwordreset_reset_v1(reset_code, new_password):
    user = get_user_by_code(reset_code)
    if user is None:
        raise InputError(description="reset_code is not a valid reset code")

    if len(new_password) < 6:
        raise InputError(description="Password entered is less than 6 characters long")

    user.hashed_password = hash_password(new_password)
    return {}


#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


# check if email entered is valid
def is_email_valid(email):
    if email is None:
        return False
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return False


def get_user_by_code(reset_code):
    if reset_code is None:
        return None
    for user in data['class_users']:
        if user.reset_code == reset_code:
            return user
    return None


def get_user_by_token(token):
    if token is None:
        return None
    session_dict = token_to_session(token)
    if session_dict is None:
        return None

    session_id = session_dict['sessionID']
    for user in data['class_users']:
        s = set(user.current_sessions)
        if session_id in s:
            return user
    return None


def get_user_session_by_token(token):
    if token is None:
        return None
    session_dict = token_to_session(token)
    if session_dict is None:
        return None

    session_id = session_dict['sessionID']
    for user in data['class_users']:
        s = set(user.current_sessions)
        if session_id in s:
            result = [user, session_id]
            return result
    return None


# return the specific user with the auth_user_id
# the user is a class
def get_user_by_uid(u_id):
    if u_id is None:
        return None
    for user in data['class_users']:
        if user.u_id == u_id:
            return user

    return None


# return the specific user with email
# the user is a class
def get_user_by_email(email):
    if email is None:
        return None
    for user in data['class_users']:
        if user.email == email:
            return user

    return None


# return the specific user with handle_str
# the user is a class
def get_user_by_handle(handle):
    if handle is None:
        return None
    for user in data['class_users']:
        if user.handle_str == handle:
            return user

    return None


# check the InputError for auth_register
def auth_register_check_error(email, password, name_first, name_last):
    # if the email address is invalid
    if not is_email_valid(email):
        raise InputError(description='Email address is not valid')

    # if the length of password is less than 6
    if len(password) < 6:
        raise InputError(description='Password length is less than 6')

    # if name_first is not between 1 and 50 characters
    if not (1 <= len(name_first) <= 50):
        raise InputError(description='name_first is not between 1 and 50 characters')

    # is name_last is not between 1 and 50 characters
    if not (1 <= len(name_last) <= 50):
        raise InputError(description='name_last is not between 1 and 50 characters')

    # if the user has regiestered before
    # which means the email address is already used by another user
    for user in data['class_users']:
        if email == user.email:
            raise InputError(description='Email address is already being used')


# create a new u_id
def create_uid():
    u_id = len(data['class_users'])
    return u_id


# create a new auth_user_id
def create_auth_user_id(u_id):
    return u_id


def create_reset_code():
    code = ''
    for _i in range(4):
        code += str(random.randint(0, 9))
    return code


# generate a new session id
def create_session_id():
    new_id = data['session_num']
    data['session_num'] = data['session_num'] + 1
    return new_id


def session_to_token(session_id):
    return jwt.encode({'sessionID': session_id}, data['secret'], algorithm='HS256')


def token_to_session(token):
    try:
        decode_session = jwt.decode(token, data['secret'], algorithms=['HS256'])
        return decode_session
    except:
        return None


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# return a concatenation of a lowercase - only
# first name and last name. If the concatenation is
# longer than 20 characters, it is cutoff at 20 characters
def full_name_20(name_first, name_last):
    full_name = name_first + name_last
    if len(full_name) > 20:
        full_name = list(full_name)[:20]
        full_name = ''.join(full_name)
    full_name = full_name.lower()
    return full_name


# create a new handle
def create_handle(name_first, name_last):
    name = full_name_20(name_first, name_last)
    count = 0

    # count the number of registered users with
    # the same concatenated name
    for user in data['class_users']:
        exist_name = full_name_20(user.name_first, user.name_last)
        if name == exist_name:
            count += 1

    # if the concatenated name is unique
    # the handle is the name
    if count == 0:
        return name
    # if the concatenated name is already taken
    # append the concatenated name with the smallest number
    # to form a new handle
    else:
        count -= 1
        handle = name + str(count)
        return handle


def create_permission(u_id):
    if u_id == 0:
        return Permission.global_owner
    else:
        return Permission.global_member


# check the login errors
# which include invalid email address,
# the email entered does not belong to a user
# and the password is incorrect
def auth_login_error_check(email, password):
    if not is_email_valid(email):
        raise InputError(description='Email address is not valid')

    user = get_user_by_email(email)
    if user is None:
        raise InputError(description='Email entered does not belong to a user')

    if user.hashed_password != hash_password(password):
        raise InputError(description='Password is not correct')
