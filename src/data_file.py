"""
Define different classes and data structures
By Lan Lin
"""


class User:
    def __init__(self, u_id, email, password, name_first, name_last, handle_str, auth_user_id, role):
        self.u_id = u_id
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = handle_str
        self.auth_user_id = auth_user_id
        self.role = role
        # not sure any other role types, like global owner?????
        # may modify this later
        if self.role not in ['owner', 'member']:
            raise Exception("role must be 'owner' or 'member")

        self.part_of_channel = []  # a list of all channels that the authorised user is part of

    def return_type_user(self):
        """in 6.1.1 Data Types
            (outputs only) named exactly user
            Dictionary containing u_id, email, name_first, name_last, handle_str
        """
        return {
            'u_id': self.u_id,
            'email': self.email,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'handle_str': self.handle_str
        }


class Channel:
    def __init__(self, name, channel_id, is_public):
        self.name = name
        self.channel_id = channel_id
        self.is_public = is_public
        if not isinstance(self.is_public, bool):        # is_public must be type of bool
            raise TypeError("is_public must be bool")
        self.all_members = []    # a list of all members of the channel
        self.owner_members = []  # a list of all owners of the channel
        self.messages = []
        self.start = -1
        self.end = -1

    def return_type_channel(self):
        """dictionary contains types { channel_id, name }"""
        return {
            'channel_id': self.channel_id,
            'name': self.name
        }


class Message:
    def __init__(self, message_id, u_id, message, time_created, channel_id):
        self.message_id = message_id
        self.u_id = u_id
        self.message = message
        self.time_created = time_created
        self.channel_id = channel_id

    def return_type_message(self):
        """
        dictionary contains types
        { message_id, u_id, message, time_created }
        """
        return {
            'message_id': self.message_id,
            'u_id': self.u_id,
            'message': self.message,
            'time_created': self.time_created
        }


data = {
    # a list of class User
    'class_users': [],
    # a list of class Channel
    'class_channels': [],
    # a list of class Message
    'class_messages': []
}

"""
Methods to use class
"""
if __name__ == '__main__':
    # Method 1: directly give paramaters, be careful about the sequence and type of inputs
    try:
        user1 = User(1, '123@gmail.com', '123ifks3', 'Hayden', 'Smith', 'handle', '1234', 'owners')
        print(f"The uid of the user1 is {user1.u_id}")
        print(f"The role of the user1 is {user1.name_last}")
    except Exception as e:
        print(f"Error! {e}")

    # Method 2:
    channel1 = Channel(name='Channel of Hayden', channel_id=1, is_public=True)
    print(f"is_public of channel1 is {channel1.is_public}")
    try:
        channel2 = Channel(name='Channel of Andrew', channel_id=2, is_public='Yes')
    except TypeError as e:
        print(f"Error! {e}")
