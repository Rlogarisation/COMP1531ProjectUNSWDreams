# Here is the tests for Bonus functions
from src.bonus import asciimoji_export, asciimoji_import
from src.message import message_send_v2, message_senddm_v1
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1, get_user_by_token
from src.channels import channels_create_v1
from src.channel import channel_messages_v1
from src.dm import dm_create_v1, dm_messages_v1
import os


def test_send_asciimoji_to_channel():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]

    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")["auth_user_id"]

    channel_0_id = channels_create_v1(token_0, "channel_0", True)["channel_id"]

    message_send_v2(token_0, channel_0_id, "<acid> i am acid, lol.")

    channel_msgs = channel_messages_v1(token_0, channel_0_id, 0)
    assert len(channel_msgs['messages']) == 1
    assert channel_msgs['messages'][0]['message'] == "⊂(◉‿◉)つ i am acid, lol."
    clear_v1()


def test_send_asciimoji_to_dm():
    clear_v1()
    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]

    u_id_0 = auth_login_v1("test_email0@gmail.com", "password")["auth_user_id"]
    u_id_1 = auth_login_v1("test_email1@gmail.com", "password")["auth_user_id"]

    dm_0_id = dm_create_v1(token_0, [u_id_1])["dm_id"]

    message_senddm_v1(token_0, dm_0_id, "<acid> i am acid, lol.")

    dm_msgs = dm_messages_v1(token_0, dm_0_id, 0)
    assert len(dm_msgs['messages']) == 1
    assert dm_msgs['messages'][0]['message'] == "⊂(◉‿◉)つ i am acid, lol."
    clear_v1()


def test_asciimoji_import():
    clear_v1()

    token_0 = auth_register_v1("test_email0@gmail.com", "password", "First0", "Last0")["token"]

    user_0 = get_user_by_token(token_0)
    user_name = user_0.name_first + user_0.name_last
    extra_asciimoji = open(f"{user_name}_asciimoji.txt", "w")
    extra_asciimoji.write(str({"<creep>": "ԅ(≖‿≖ԅ)", "crim3s": "( ✜︵✜ )", "cute": "(｡◕‿‿◕｡)"}))
    extra_asciimoji.close()

    asciimoji_import(token_0)

    assert user_0.asciimoji == {"<acid>": "⊂(◉‿◉)つ", "<afraid>": "(ㆆ _ ㆆ)", "<angry>": "•`_´•", "<catlenny>": "( ͡° ᴥ ͡°)", "<creep>": "ԅ(≖‿≖ԅ)", "crim3s": "( ✜︵✜ )", "cute": "(｡◕‿‿◕｡)"}
    os.system(f"rm -rf {user_name}_asciimoji.txt")
    clear_v1()


def test_asciimoji_export():
    clear_v1()
    token_1 = auth_register_v1("test_email1@gmail.com", "password", "First1", "Last1")["token"]

    user_1 = get_user_by_token(token_1)
    asciimoji_export(token_1)

    user_name = user_1.name_first + user_1.name_last
    check_export = open(f"{user_name}_asciimoji.txt", "r")

    assert check_export.read() == str({"<acid>": "⊂(◉‿◉)つ", "<afraid>": "(ㆆ _ ㆆ)", "<angry>": "•`_´•", "<catlenny>": "( ͡° ᴥ ͡°)"})
    os.system(f"rm -rf {user_name}_asciimoji.txt")
    clear_v1()
