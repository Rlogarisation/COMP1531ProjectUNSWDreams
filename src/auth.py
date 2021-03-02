import re
from .data_file import User, data
from .error import InputError


# check if email entered is valid
def is_email_valid(email):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return False


# return the specific user with the auth_user_id
# the user is a class
def get_user_by_auth_id(auth_user_id):
    for user in data['class_users']:
        if user.auth_user_id == auth_user_id:
            return user

    return None


# return the specific user with email
# the user is a class
def get_user_by_email(email):
    for user in data['class_users']:
        if user.email == email:
            return user

    return None


# check the InputError for auth_register
def auth_register_check_error(email, password, name_first, name_last):
    # if the email address is invalid
    if not is_email_valid(email):
        raise InputError('Email address is not valid')

    # if the length of password is less than 6
    if len(password) < 6:
        raise InputError('Password length is less than 6')

    # if name_first is not between 1 and 50 characters
    if not (1 <= len(name_first) <= 50):
        raise InputError('name_first is not between 1 and 50 characters')

    # is name_last is not between 1 and 50 characters
    if not (1 <= len(name_last) <= 50):
        raise InputError('name_last is not between 1 and 50 characters')

    # if the user has regiestered before
    # which means the email address is already used by another user
    for user in data['class_users']:
        if email == user.email:
            raise InputError('Email address is already being used')


# create a new u_id
def create_uid():
    u_id = len(data['class_users'])
    return u_id


# create a new auth_user_id
def create_auth_user_id(u_id):
    return u_id


# return a concatenation of a lowercase - only
# first name and last name. If the concatenation is
# longer than 20 characters, it is cutoff at 20 characters
def full_name_20(name_first, name_last):
    full_name = name_first + name_last
    if len(full_name) > 20:
        full_name = list(full_name)[:20]
        full_name = ''.join(full_name)
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
        count_len = len(str(count))
        char_len = 20 - count_len
        name = list(name)[:char_len]
        name = ''.join(name)
        handle = name + str(count)
        return handle


def create_role(u_id):
    if u_id == 0:
        return 'global owner'
    else:
        return 'global member'


# Given a user's first and last name, email address, and password,
# create a new account for them and return a new `auth_user_id`
def auth_register_v1(email, password, name_first, name_last):
    auth_register_check_error(email, password, name_first, name_last)

    u_id = create_uid()
    auth_user_id = create_auth_user_id(u_id)
    handle = create_handle(name_first, name_last)
    role = create_role(u_id)

    user_ = User(u_id, email, password, name_first, name_last, handle, auth_user_id, role)
    data['class_users'].append(user_)

    # return {
    #     'auth_user_id': 1,
    # }
    return {
        'auth_user_id': auth_user_id
    }


# check the login errors
# which include invalid email address,
# the email entered does not belong to a user
# and the password is incorrect
def auth_login_error_check(email, password):
    if not is_email_valid(email):
        raise InputError('Email address is not valid')

    user = get_user_by_email(email)
    if user is None:
        raise InputError('Email entered does not belong to a user')

    if user.password != password:
        raise InputError('Password is not correct')


# Given a registered users' email and password
# and returns their `auth_user_id` value
def auth_login_v1(email, password):
    auth_login_error_check(email, password)

    user = get_user_by_email(email)
    return {
        'auth_user_id': user.auth_user_id
    }

    # return {
    #     'auth_user_id': 1,
    # }
