from flask_login import UserMixin
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user_id, username, roles):
        self.user_id = ObjectId(user_id)  # Store as ObjectId for consistency with MongoDB
        self.username = username
        self.roles = roles

    def get_id(self):
        # Flask-Login expects the user identifier to be a unicode string
        return str(self.user_id)

