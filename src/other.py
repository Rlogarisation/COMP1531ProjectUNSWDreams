from src.data_file import data, DATA, dump_data


"""
Author: Lan Lin

Background
Resets the internal data of the application to it's initial state
"""


def clear_v1():
    data['class_users'] = []
    data['class_channels'] = []
    data['class_dms'] = []
    data['session_num'] = 0
    data['message_num'] = 0
    data['secret'] = 'THIS_IS_SECRET'
    dump_data(DATA)
    return {}


def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
