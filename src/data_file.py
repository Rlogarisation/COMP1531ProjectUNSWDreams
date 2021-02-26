"""
Define different classes and data structures
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
        self.part_of_channel = []           # a list of all channels that the authorised user is part of

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
        self.all_members = []              # a list of all members of the channel
        self.owner_members = []            # a list of all owners of the channel
        self.messages = []

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
