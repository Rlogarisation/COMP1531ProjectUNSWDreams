import pytest
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v2, auth_logout, get_user_by_token
from src.error import InputError, AccessError
from src.channel import channel_details_v1, channel_invite_v1, channel_join_v1
from src.channels import channels_create_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1, users_all, admin_user_remove, admin_userpermission_change
from src.data_file import Permission
#############################################################################
#                                                                           #
#                       Test for admin_user_permission_change               #
#                                                                           #
#############################################################################


def test_invalid_token():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    token = register1['token']
    invalid_token = f"{token}123"
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    u_id2 = register2['auth_user_id']
    new_permission_id = Permission.global_owner
    with pytest.raises(AccessError):
        admin_userpermission_change(invalid_token, u_id2, new_permission_id)


def test_admin_change_permission_invalid_owner():
    clear_v1()
    auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    register3 = auth_register_v2('haha1@gmail.com', '1231231231', 'Pete', 'Whit')
    token2 = register2['token']
    uid3 = register3['auth_user_id']
    with pytest.raises(AccessError):
        admin_userpermission_change(token2, uid3, Permission.global_owner)


def test_admin_change_permission_invalid_user():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid2 = register2['auth_user_id']
    invalid_uid = uid2 + 100
    with pytest.raises(InputError):
        admin_userpermission_change(token1, invalid_uid, Permission.global_owner)


def test_admin_change_permission_invalid_permission():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid2 = register2['auth_user_id']
    invalid_permission = 3
    with pytest.raises(InputError):
        admin_userpermission_change(token1, uid2, invalid_permission)


def test_admin_change_permission_owner():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = register1['token']
    uid2 = register2['auth_user_id']
    token2 = register2['token']
    admin_userpermission_change(token1, uid2, Permission.global_owner)
    channel_id = channels_create_v1(token1, "My Channel", False)['channel_id']
    channel_join_v1(token2, channel_id)


def test_admin_change_permission_member():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
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
def test_admin_user_remove_invalid_uid():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = register1['token']
    with pytest.raises(InputError):
        admin_user_remove(token1, None)
    with pytest.raises(InputError):
        admin_user_remove(token1, 'hehe')


def test_admin_user_remove_only_owner():
    clear_v1()
    register1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = register1['token']
    uid1 = register1['auth_user_id']
    with pytest.raises(InputError):
        admin_user_remove(token1, uid1)


def test_admin_user_remove_invalid_owner():
    clear_v1()
    auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token2 = register2['token']
    uid2 = register2['auth_user_id']
    with pytest.raises(AccessError):
        admin_user_remove(token2, uid2)


def test_admin_user_remove_successfully():
    clear_v1()
    regiester1 = auth_register_v2('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v2('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
    token1 = regiester1['token']
    token2 = register2['token']
    uid2 = register2['auth_user_id']
    user_profile2 = user_profile_v1(token2, uid2)
    assert user_profile2['user']['email'] == 'test@testexample.com'
    admin_user_remove(token1, uid2)
    user_profile2 = user_profile_v1(token1, uid2)
    assert user_profile2['user']['name_first'] == 'Removed user'
    assert user_profile2['user']['name_last'] == 'Removed user'
