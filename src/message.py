from src.data_file import data

def message_send_v1(auth_user_id, channel_id, message):
    for i in data["class_channels"]:
        if i.channel_id == channel_id:
            i.messages.insert(0,message)
            break

    return {
        'message_id': 1,
    }


def message_remove_v1(auth_user_id, message_id):
    return {
    }


def message_edit_v1(auth_user_id, message_id, message):
    return {
    }
