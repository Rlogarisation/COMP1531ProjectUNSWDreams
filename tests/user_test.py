import pytest
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, auth_logout, get_user_by_token
from src.error import InputError, AccessError
from src.channel import channel_details_v1, channel_invite_v1
from src.channels import channels_create_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1,
users_all, admin_user_remove, admin_userpermission_change

#############################################################################
#                                                                           #
#                       Test for admin_user_remove                          #
#                                                                           #
#############################################################################
