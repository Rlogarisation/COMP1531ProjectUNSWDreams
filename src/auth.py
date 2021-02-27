import re
from data_file import User


def is_email_valid(email):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return False


def get_class_user(auth_user_id):
    user1 = User(auth_user_id, '123@gmail.com', '123ifks3', 'Hayden', 'Smith', 'handle', '1234', 'owner')
    return user1


def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }


def auth_register_v1(email, password, name_first, name_last):
    return {
        'auth_user_id': 1,
    }
