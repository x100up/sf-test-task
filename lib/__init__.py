from urlparse import urlparse

class AuthError(BaseException):
    pass


class AuthExtension(object):
    ext_name = 'auth_extension'

    def __init__(self, app):
        """
        Create auth extension
        :param app:
        :type app: flask.app.Flask
        :return:
        """
        if self.ext_name not in app.extensions:
            self.init_app(app)

    def init_app(self, app):
        """
        Init auth extension
        :param app:
        :type app: flask.app.Flask
        :return:
        """
        types = app.config.get('AUTH_PROVIDERS')
        db_uri = app.config.get('DATABASE_URI')

        # init user`s builder
        self.providers = {}
        for t in types:
            module = __import__(__name__ + '.provider.' + t, fromlist=['User'])
            self.providers[t] = module.User

        # init data storage
        uri = urlparse(db_uri)

        if not uri.scheme:
            raise ValueError('')

        if uri.scheme == 'mongodb':
            from lib.storage.mongo import AuthStorage
            self.storage = AuthStorage(db_uri)
        else:
            # TODO filter sql scheme
            from lib.storage.sql import AuthStorage
            self.storage = AuthStorage(db_uri)

        # save to app context
        app.extensions[self.ext_name] = self

    def build_user(self, user_type, user_data):
        """
        Build user data object
        :param user_type:
        :param user_data:
        :return:
        """
        if user_type in self.providers:
            if user_type not in self.providers:
                raise AuthError('Unknown user type')

            return self.providers[user_type](**user_data)

    def get_token(self, user):
        """
        Get token for user
        :param user:
        :type user: lib.provider.BaseUser
        :return:
        """
        self.storage.get_token(user)

    def save_user(self, user):
        """
        Save user to data storage
        :param user:
        :type user: lib.provider.BaseUser
        :return:
        """
        self.storage.save_user(user)