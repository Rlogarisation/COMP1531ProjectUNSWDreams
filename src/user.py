from src.data_file import Permission, data
from src.auth import get_user_by_uid, session_to_token, token_to_session, get_user_by_token, \
    is_email_valid
from src.error import InputError, AccessError
"""
user.py
Auther: Lan Lin
"""


def user_profile_v1(token, u_id):
    # find the user to show the profile
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    user = get_user_by_uid(u_id)
    if user is None:
        raise InputError(description="User with u_id is not a valid user")

    result = user.return_type_user()
    return {
        'user': result
    }


def user_profile_setname_v1(token, name_first, name_last):
    # find the user to update the name
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    # if name_first is not between 1 and 50 characters
    if not (1 <= len(name_first) <= 50):
        raise InputError(description='name_first is not between 1 and 50 characters')

    # is name_last is not between 1 and 50 characters
    if not (1 <= len(name_last) <= 50):
        raise InputError(description='name_last is not between 1 and 50 characters')

    user.name_first = name_first
    user.name_last = name_last
    return {}


def user_profile_setemail_v1(token, email):
    # find the user to update the email
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    # if the email address is invalid
    if not is_email_valid(email):
        raise InputError(description='Email address is not valid')

    # if the user has regiestered before
    # which means the email address is already used by another user
    for u in data['class_users']:
        if email == u.email:
            raise InputError(description='Email address is already being used')

    user.email = email
    return {}


def user_profile_sethandle_v1(token, handle_str):
    # find the user to update the handle
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    # is handle_str is not between 3 and 20 characters
    if not (3 <= len(handle_str) <= 20):
        raise InputError(description='handle_str is not between 3 and 52 characters')

    # if the handle_str is already used by another user
    for u in data['class_users']:
        if handle_str == u.handle_str:
            raise InputError(description='handle_str is already being used')

    user.handle_str = handle_str
    return {}


def users_all(token):
    # Pull the data of user from data_file
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="user does not refer to a vaild user")

    list_return = []
    for i in data['class_users']:
        list_return.append(i.return_type_user())
    return {
        'users': list_return
    }


def admin_user_remove(token, u_id):
    # find the owner to implement the remove
    owner = get_user_by_token(token)
    if owner is None:
        raise AccessError(description="Token passed in is invalid")
    if owner.permission_id != Permission.global_owner:
        raise AccessError(description="The authorised user is not a Dream owner")

    # find the user to be removed
    user = get_user_by_uid(u_id)
    if user is None:
        raise InputError(description="User with u_id is not a valid user")

    # if the user is the only owner, the user cannot be removed
    num_dream_owners = count_dream_owner()
    if user.permission_id == Permission.global_owner and num_dream_owners == 1:
        raise InputError(description="The user is currently the only owner")

    # the user first name and last name is replaced by 'Remove user'
    # if the user can be removed successfully
    user.name_first = user.name_last = 'Removed user'

    # deal with the messages the removed user sent in channels
    for channel in data['class_channels']:
        for msg in channel.messages:
            if msg.u_id == user.u_id:
                msg.message = 'Removed user'

    # deal with the messages the removed user sent in channels
    for dm in data['class_dms']:
        for msg in dm.messages:
            if msg.u_id == user.u_id:
                msg.message = 'Removed user'

    return {}


def admin_userpermission_change(token, u_id, permission_id):
    owner = get_user_by_token(token)
    if owner is None:
        raise AccessError(description="Token passed in is invalid")
    if owner.permission_id != Permission.global_owner:
        raise AccessError(description="The authorised user is not a Dream owner")
    user = get_user_by_uid(u_id)
    if user is None:
        raise InputError(description="User with u_id is not a valid user")
    if not (permission_id == Permission.global_owner or permission_id == Permission.global_member):
        raise InputError(description="permission_id does not refer to a value permission")

    user.permission_id = permission_id
    return {}
#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


def count_dream_owner():
    count = 0
    for user in data['class_users']:
        if user.permission_id == Permission.global_owner:
            count += 1
    return count

