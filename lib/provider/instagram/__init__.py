from lib.provider import BaseUser
import json


class User(BaseUser):
    def __init__(self, **entries):
        self.email = None
        self.instagram_id = None
        self.instagram_token = None
        self.refresh_token = None
        super(User, self).__init__(**entries)

    def is_valid(self):
        return self.email and self.instagram_id and self.instagram_token and self.refresh_token

    @property
    def auth_code(self):
        return self.instagram_token

    @property
    def provider(self):
        return 'instagram'

    @property
    def extra_data(self):
        return json.dumps({'instagram_id': self.instagram_id, 'instagram_token': self.instagram_token,
                           'refresh_token': self.refresh_token})
