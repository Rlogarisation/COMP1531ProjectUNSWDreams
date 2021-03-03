from .data_file import data
<<<<<<< HEAD
=======
# from data_file import data
>>>>>>> master


def clear_v1():
    data['class_users'] = []
    data['class_channels'] = []
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
