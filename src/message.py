from src.data_file import data
from src.error import InputError, AccessError


def message_send_v1(auth_user_id, channel_id, message):
    for i in data["class_channels"]:
        if i.channel_id == channel_id:
            i.messages.insert(0, message)
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


#############################################################################
#                                                                           #
#                              Helper function                              #
#                                                                           #
#############################################################################


# generate a new session id
def create_session_id():
    new_id = data['message_num']
    data['message_num'] = data['message_num'] + 1
    return new_id
