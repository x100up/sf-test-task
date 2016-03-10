from lib.provider import BaseUser
import json


class User(BaseUser):
    def __init__(self, **entries):
        self.email = None
        self.facebook_id = None
        self.facebook_token = None
        super(User, self).__init__(**entries)

    def is_valid(self):
        return self.email and self.facebook_id and self.facebook_token

    @property
    def auth_code(self):
        return self.facebook_token

    @property
    def provider(self):
        return 'facebook'

    @property
    def extra_data(self):
        return json.dumps({'facebook_id': self.facebook_id, 'facebook_token': self.facebook_token})
