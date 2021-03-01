from .data_file import data


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


register1 = auth_register_v1('haha@gmail.com', '123', 'Peter', 'White')
register2 = auth_register_v1('test@testexample.com', 'wp01^#$dp1o23', 'Tom', 'Green')
auth_user_id1 = register1['auth_user_id']
auth_user_id2 = register2['auth_user_id']

user1 = get_class_user(auth_user_id1)
user2 = get_class_user(auth_user_id2)
print(user1.handle_str)
