from src.data_file import Permission, data
from src.auth import get_user_by_uid, session_to_token, token_to_session, get_user_by_token, \
    is_email_valid
from src.error import InputError, AccessError
from PIL import Image
import requests
import os
import urllib.request
"""
user.py
Auther: Lan Lin
"""


def user_profile_v1(token, u_id):
    # find the user to show the profile
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    user_ = get_user_by_uid(u_id)
    if user_ is None:
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
    user.name_first = 'Removed'
    user.name_last = 'user'
    # deal with the messages the removed user sent in channels
    for channel in data['class_channels']:
        for msg in channel.messages:
            if msg.u_id == user.u_id:
                msg.message = 'Removed user'

    # deal with the messages the removed user sent in channels
    for dm in data['class_dms']:
        for msg in dm.dm_messages:
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


def user_stats_v1(token):
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    num1 = len(user.part_of_channel) + len(user.part_of_dm) + len(user.messages)
    num2 = len(data['class_channels']) + len(data['class_dms']) +len(data['class_messages'])
    involvement_rate = num1/num2

    user_stats = {
        'channels_joined': user.channels_joined,
        'dms_joined': user.dms_joined,
        'messages_sent': user.messages_sent,
        'involvement_rate': involvement_rate
    }

    return {
        'user_stats': user_stats
    }


def users_stats_v1(token):
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    num1 = num_user_in_channel_dm()
    num2 = len(data['class_users'])
    utilization_rate = num1/num2

    dreams_stats = {
        'channels_exist': data['channels_exist'],
        'dms_exist': data['dms_exist'],
        'messages_exist': data['messages_exist'],
        'utilization_rate': utilization_rate
    }

    return {
        'dreams_stats': dreams_stats
    }


def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    # get the image, check the image
    response = requests.get(img_url, stream=True)
    if response.status_code != 200:
        raise InputError(description="img_url returns an HTTP status other than 200.")

    image = Image.open(response.raw)
    if image.format != 'JPEG':
        raise InputError(description="Image uploaded is not a JPG")

    width, height = image.size
    if x_start > width or x_end > width or x_start < 0 or x_end < 0 or x_start >= x_end:
        raise InputError(description="x_start or x_end are not within the dimensions of the image")
    if y_start > height or y_end > height or y_start < 0 or y_end < 0 or y_start >= y_end:
        raise InputError(description="y_start or y_end are not within the dimensions of the image")

    # save the original image locally
    path = os.getcwd() + '/src/static/'
    # path = './src/static'
    if not os.path.exists(path):
        os.mkdir(path)
    path = path + str(user.u_id) + '.jpg'
    # urllib.request.urlretrieve(img_url, path)

    # crop the image
    image_cropped = image.crop((x_start, y_start, x_end, y_end))
    # overwrite the original image by the cropped image
    image_cropped.save(path)
    user.image_url = path

    return user
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


def num_user_in_channel_dm():
    count = 0
    for user in data['class_users']:
        num_channel_dm = len(user.part_of_channel) + len(user.part_of_dm)
        if num_channel_dm > 0:
            count += 1
    return count
