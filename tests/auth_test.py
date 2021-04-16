from datetime import datetime
from threading import local
from time import sleep, localtime, mktime, strftime, strptime
import pytest
import poplib
import base64
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from src.other import clear_v1
from src.auth import auth_login_v1, auth_register_v1, auth_logout, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.error import InputError, AccessError
from src.channel import channel_details_v1, channel_invite_v1
from src.channels import channels_create_v1
"""
Author: Lan Lin

Test for auth_register_v1 function implementation

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
#                       Test for auth_register_v1                           #
#                                                                           #
#############################################################################


# test email does not match the regular expression
def test_auth_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('123.com', '12345ufd', 'Lan', 'Lin')
    with pytest.raises(InputError):
        auth_register_v1('abc@@@.com', '0823hdskhji', 'Langley', 'Lin')
    # with pytest.raises(InputError):
    #     auth_register_v1(None, "password", 'Lan', 'Lin')

    clear_v1()

# test email address is already being used by another user


def test_auth_register_duplicate_email():
    clear_v1()
    auth_register_v1('haha1@gmail.com', 'shkdlch', 'Peter', 'White')
    with pytest.raises(InputError):
        auth_register_v1('haha1@gmail.com', '0w9epodu', 'Tom', 'White')

    clear_v1()

# test for password entered is less than 6 characters long


def test_auth_register_pwd_length():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123', 'Tom', 'White')
    with pytest.raises(InputError):
        auth_register_v1('haha2@gmail.com', 'ab#', 'Peter', 'White')

    clear_v1()

# name_first is not between 1 and 50 characters inclusively in length


def test_auth_register_firstName_length():
    clear_v1()
    name = 'a' * 51
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123iwuiused', '', 'White')
    with pytest.raises(InputError):
        auth_register_v1('haha2@gmail.com', 'iwsdrjcio', name, 'White')

    clear_v1()

# name_last is not between 1 and 50 characters inclusively in length


def test_auth_register_lastName_length():
    clear_v1()
    name = 'a' * 51
    with pytest.raises(InputError):
        auth_register_v1('haha@gmail.com', '123kjsldfiew', 'Peter', '')
    with pytest.raises(InputError):
        auth_register_v1('haha2@gmail.com', 'iwsdcio3', 'Tom', name)

    clear_v1()

# test several users can successfully register


def test_auth_register_valid_small():
    clear_v1()
    # register two users with valid inputs
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
    token1 = register1['token']
    token2 = register2['token']
    assert auth_user_id1 != auth_user_id2
    assert token1 != token2

    clear_v1()

# test large number of users can register successfully


def test_auth_register_valid_large():
    clear_v1()
    id_list = []
    for index in range(50):
        person = auth_register_v1('example'+str(index)+'@testexample.com', 'abcuief98dh', 'Tom', 'Green')
        # check the auth_user_id generated is correct
        assert person['auth_user_id'] == index
        id_list.append(person['auth_user_id'])

    # check all auth_user_ids are unique
    # check the number of registered users are correct
    assert len(set(id_list)) == len(id_list) == 50

    clear_v1()

# test if a valid handle is generated


def test_auth_register_handle_valid():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'zxcvbnmasdfg', 'hjklqwe')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#123', 'zxcvbnmasdfg', 'hjklqwert')
    register3 = auth_register_v1('haha2@gmail.com', '123jcqewp2', 'zxcvbnmasdfg', 'hjklqwert')
    register4 = auth_register_v1('haha3@gmail.com', '123jcqewp2', 'zxcvbnmasdfg', 'hjklqwertiowjec')

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
    assert member3['handle_str'] == 'zxcvbnmasdfghjklqwer0'
    assert member4['handle_str'] == 'zxcvbnmasdfghjklqwer1'

    clear_v1()


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
#                       Test for auth_login_v1                              #
#                                                                           #
#############################################################################


# test for email entered is not a valid email
def test_auth_login_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('123.@com', '12345ufd')
    with pytest.raises(InputError):
        auth_login_v1('a.,#0@test.com', '0823hdskhji')
    with pytest.raises(InputError):
        auth_login_v1(None, 'password')

    clear_v1()

# test for email entered does not belong to a user


def test_auth_login_not_registered_email():
    clear_v1()
    # register a user
    auth_register_v1('haha@gmail.com', '123123123', 'Tom', 'Green')
    # login the user with not registered email
    # will give error
    with pytest.raises(InputError):
        auth_login_v1('haha2@gmail.com', '123123123')

    clear_v1()

# test for password is not correct


def test_auth_login_wrong_password():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'Green')
    with pytest.raises(InputError):
        auth_login_v1('haha@gmail.com', 'jfqowei0-23opj')

    clear_v1()

# test for users can login successfully


def test_auth_login_valid():
    clear_v1()
    # register two users with valid inputs
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')

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

    clear_v1()

# test for the same user with different sessions


def test_auth_login_different_sessions():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')

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

    clear_v1()
#############################################################################
#                                                                           #
#                       Test for auth_logout                                #
#                                                                           #
#############################################################################


def test_auth_logout_invalid_token():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token = register1['token']
    invalid_token = f"{token}123"
    assert auth_logout(invalid_token) == {'is_success': False}
    assert auth_logout(None) == {'is_success': False}

    clear_v1()


def test_auth_logout_successfully_emall():
    clear_v1()
    register1 = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token1 = register1['token']
    # user1 = get_user_by_token(token1)
    login2 = auth_login_v1('haha@gmail.com', '123123123')
    # assert len(user1.current_sessions) == 2
    token2 = login2['token']
    assert auth_logout(token1) == {'is_success': True}
    # assert len(user1.current_sessions) == 1
    assert auth_logout(token2) == {'is_success': True}
    # assert len(user1.current_sessions) == 0

    clear_v1()


def test_auth_logout_successfully_large():
    clear_v1()
    auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
    token_list = []
    for _i in range(20):
        login = auth_login_v1(f'haha@gmail.com', '123123123')
        token_list.append(login['token'])
    for token in token_list:
        result = auth_logout(token)
        assert result == {'is_success': True}

    clear_v1()
#############################################################################
#                                                                           #
#   Test for auth_passwordreset_request_v1 and auth_passwordreset_reset_v1  #
#                                                                           #
#############################################################################


def test_auth_passwordreset_successful():
    clear_v1()
    id_check = auth_register_v1('styuannj@163.com', '123123123', 'Peter', 'White')['auth_user_id']
    auth_passwordreset_request_v1('styuannj@163.com')['reset_code']

    # # email sent timestamp
    # time_stamp_1 = mktime(localtime())

    sleep(2)
    msg = get_email_content("styuannj@163.com", "UXRVCTIAEQZVVGAG", "pop.163.com")

    # # email received timestamp
    # email_sent_time = list(msg['Date'].split())
    # del email_sent_time[5]
    # string_time = strptime(' '.join(email_sent_time), "%a, %d %b %Y %H:%M:%S (%Z)")
    # time_stamp_2 = mktime(string_time)

    # # timestamp checking
    # assert time_stamp_1 - 2 <= time_stamp_2 <= time_stamp_1 + 2

    reset_code = parser_reset_code(msg)

    auth_passwordreset_reset_v1(reset_code, 'TheNewPassword')
    assert auth_login_v1('styuannj@163.com', 'TheNewPassword')['auth_user_id'] == id_check

    clear_v1()


def test_auth_passwordrequest_invalid_email():
    clear_v1()
    auth_register_v1('cblinker17@gmail.com', '123123123', 'Peter', 'White')
    with pytest.raises(InputError):
        auth_passwordreset_request_v1('cblinker@gmail.com')

    clear_v1()


def test_auth_passwordreset_reset_invalid_password():
    clear_v1()
    auth_register_v1('cblinker17@gmail.com', '123123123', 'Peter', 'White')
    reset_code = auth_passwordreset_request_v1('cblinker17@gmail.com')['reset_code']
    invalid_password = '123'
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1(reset_code, invalid_password)

    clear_v1()


def test_auth_passwordreset_reset_invalid_reset_code():
    clear_v1()
    auth_register_v1('cblinker17@gmail.com', '123123123', 'Peter', 'White')
    reset_code = auth_passwordreset_request_v1('cblinker17@gmail.com')['reset_code']
    invalid_reset_code = reset_code + '123'
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1(invalid_reset_code, 'TheNewPassword')
    clear_v1()

# """
# Author : Emir Aditya Zen

# Test for auth_passwordreset_request_v1 and auth_passwordreset_reset_v1 function implementation

# Tests content:
# 1. Succesful implementation of both functions
# 3. Invalid reset_code
# 4. New password less than 6 characters
# """
# #############################################################################
# #                                                                           #
# #   Test for auth_passwordreset_request_v1 and auth_passwordreset_reset_v1  #
# #                                                                           #
# #############################################################################


# def test_auth_passwordreset_successful():
#     clear_v1()
#     id_check = auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')['auth_user_id']
#     reset_code = auth_passwordreset_request_v1('haha@gmail.com')['reset_code']
#     auth_passwordreset_reset_v1(reset_code, 'TheNewPassword')
#     assert auth_login_v1('haha@gmail.com', 'TheNewPassword')['auth_user_id'] == id_check


# def test_auth_passwordreset_reset_invalid_password():
#     clear_v1()
#     auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
#     reset_code = auth_passwordreset_request_v1('haha@gmail.com')['reset_code']
#     invalid_password = '123'
#     with pytest.raises(InputError):
#         auth_passwordreset_reset_v1(reset_code, invalid_password)


# def test_auth_passwordreset_reset_invalid_reset_code():
#     clear_v1()
#     auth_register_v1('haha@gmail.com', '123123123', 'Peter', 'White')
#     reset_code = auth_passwordreset_request_v1('haha@gmail.com')['reset_code']
#     invalid_reset_code = reset_code + '123'
#     with pytest.raises(InputError):
#         auth_passwordreset_reset_v1(invalid_reset_code, 'TheNewPassword')


#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################

def parser_subject(msg):
    subject = msg['Subject']
    value, charset = decode_header(subject)[0]
    if charset:
        value = value.decode(charset)
    # print('邮件主题： {0}'.format(value))
    return value


def parser_address(msg):
    hdr, addr = parseaddr(msg['From'])
    # name 发送人邮箱名称， addr 发送人邮箱地址
    name, charset = decode_header(hdr)[0]
    if charset:
        name = name.decode(charset)
    # print('发送人邮箱名称: {0}，发送人邮箱地址: {1}'.format(name, addr))


def parser_content(msg):
    content = msg.get_payload()

    # 文本信息
    content_charset = content[0].get_content_charset()  # 获取编码格式
    text = content[0].as_string().split('base64')[-1]
    text_content = base64.b64decode(text).decode(content_charset)  # base64解码

    # 添加了HTML代码的信息
    content_charset = content[1].get_content_charset()
    text = content[1].as_string().split('base64')[-1]
    html_content = base64.b64decode(text).decode(content_charset)
    # print(('文本信息: {0}\n添加了HTML代码的信息: {1}'.format(text_content, html_content)))


def parser_reset_code(msg):
    content = msg.get_payload()
    reset_code = list(content.split())[-1:][0]
    return reset_code


def get_email_content(email_address, password, pop3_server):
    # 开始连接到服务器
    server = poplib.POP3(pop3_server)

    # 打开或者关闭调试信息，为打开，会在控制台打印客户端与服务器的交互信息
    server.set_debuglevel(1)

    # 打印POP3服务器的欢迎文字，验证是否正确连接到了邮件服务器
    # print(server.getwelcome().decode('utf8'))

    # 开始进行身份验证
    server.user(email_address)
    server.pass_(password)

    # 返回邮件总数目和占用服务器的空间大小（字节数）， 通过stat()方法即可
    email_num, email_size = server.stat()
    # print("消息的数量: {0}, 消息的总大小: {1}".format(email_num, email_size))

    # 使用list()返回所有邮件的编号，默认为字节类型的串
    rsp, msg_list, rsp_siz = server.list()
    # print("服务器的响应: {0},\n消息列表： {1},\n返回消息的大小： {2}".format(rsp, msg_list, rsp_siz))

    # print('邮件总数： {}'.format(len(msg_list)))

    # 下面单纯获取最新的一封邮件
    total_mail_numbers = len(msg_list)
    rsp, msglines, msgsiz = server.retr(total_mail_numbers)
    # print("服务器的响应: {0},\n原始邮件内容： {1},\n该封邮件所占字节大小： {2}".format(rsp, msglines, msgsiz))

    msg_content = b'\r\n'.join(msglines).decode('gbk')

    msg = Parser().parsestr(text=msg_content)
    # print('解码后的邮件信息:\n{}'.format(msg))
    # print("发送时间 == ", msg["Date"])

    # 关闭与服务器的连接，释放资源
    server.close()

    return msg
