import pickle
"""
Define different classes: User, Channel, Message
Define data structure: data
Written by: Lan Lin
"""


class Permission:
    global_owner = 1
    global_member = 2


class User:
    def __init__(self, u_id, email, hashed_password, name_first, name_last, handle_str, auth_user_id, permission_id):
        self.u_id = u_id
        self.email = email
        self.hashed_password = hashed_password
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = handle_str
        self.auth_user_id = auth_user_id
        self.permission_id = permission_id
        # The one who registers the first will be the global owner
        # The users who register afterward will be a global member
        # The role does not indicate the 'owner' or
        # a 'member' of a channel in this part
        # if self.role not in ['global owner', 'global member']:
        #     raise Exception("role must be 'owner' or 'member")

        # a list of all channels that the authorised user is part of
        # including the user is a memeber and the user is an owner of the channel
        self.part_of_channel = []
        self.part_of_dm = []
        self.dm_owns = []
        self.channel_owns = []  # a list of all channels that the user is the owner of the channel
        self.current_sessions = []  # a list of current sessions of the user

    def return_type_user(self):
        """in 6.1.1 Data Types
            (outputs only) named exactly user
            Dictionary containing u_id, email, name_first, name_last, handle_str
        """
        return {'u_id': self.u_id, 'email': self.email, 'name_first': self.name_first, 'name_last': self.name_last, 'handle_str': self.handle_str}


class Channel:
    def __init__(self, name, channel_id, is_public):
        self.start = -1
        self.end = -1
        self.name = name
        self.channel_id = channel_id
        self.is_public = is_public
        if not isinstance(self.is_public, bool):  # is_public must be type of bool
            raise TypeError("is_public must be bool")
        self.all_members = []  # a list of all members of the channel, including members and owners
        self.owner_members = []  # a list of all owners of the channel
        self.messages = []

    def return_type_channel(self):
        """dictionary contains types { channel_id, name }"""
        return {'channel_id': self.channel_id, 'name': self.name}


class Message:
    def __init__(self, message_id, u_id, message, time_created, channel_id, dm_id):
        self.message_id = message_id
        self.u_id = u_id
        self.message = message
        self.time_created = time_created
        self.channel_id = channel_id
        self.dm_id = dm_id

    def return_type_message(self):
        """
        dictionary contains types
        { message_id, u_id, message, time_created }
        """
        return {'message_id': self.message_id, 'u_id': self.u_id, 'message': self.message, 'time_created': self.time_created}


class DM:
    def __init__(self, dm_name, dm_id):
        self.start = -1
        self.end = -1
        self.dm_name = dm_name
        self.dm_id = dm_id
        self.dm_members = []
        self.dm_owners = []
        self.dm_messages = []

    def return_type_dm(self):
        return {'dm_id': self.dm_id, 'name': self.dm_name}


DATA = {
    # a list of class User
    'class_users': [],
    # a list of class Channel
    'class_channels': [],
    # a list of class DM
    'class_dms': [],
    # to record the number of sessions
    'session_num': 0,
    # to record the number of messages
    'message_num': 0,
    'secret': 'THIS_IS_SECRET'
}


def load_data():
    global DATA
    try:
        with open("db.p", "rb") as FILE:
            dt = pickle.load(FILE)
            return dt
    except FileNotFoundError:
        with open("db.p", "wb") as FILE:
            pickle.dump(DATA, FILE)
            return DATA


def dump_data(dt):
    with open("db.p", "wb") as FILE:
        pickle.dump(dt, FILE)


data = load_data()
