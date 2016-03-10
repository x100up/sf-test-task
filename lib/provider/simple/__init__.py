from lib.provider import BaseUser
from hashlib import md5


class User(BaseUser):
    def __init__(self, **entries):
        self.email = None
        self.password = None
        super(User, self).__init__(**entries)

    def is_valid(self):
        return self.email and self.password

    @property
    def auth_code(self):
        # TODO add salt to hash
        return md5(self.email + '@' + self.password).hexdigest()

    @property
    def provider(self):
        return 'simple'
