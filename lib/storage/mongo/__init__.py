from mongoengine import connect, Document, StringField
from lib import AuthError
from lib.storage import BaseAuthStorage


class User(Document):
    email = StringField(required=True)
    provider = StringField(required=True, unique_with='email')
    auth_code = StringField(required=True)
    data = StringField()


class AuthStorage(BaseAuthStorage):
    def __init__(self, db_uri):
        self.connection = connect('auth', host=db_uri)

    def save_user(self, user):
        """
        Save user to database
        :param user: user object
        :type user: auth.provider.BaseUser
        """
        save = User(email=user.email, provider=user.provider, auth_code=user.auth_code, data=user.extra_data).save()
        pass

    def get_token(self, user):
        """
        :param user: user object
        :type user: lib.provider.BaseUser
        :return:
        :rtype: str or unicode
        """
        q = User.objects(auth_code=user.auth_code, provider=user.provider).limit(1).count()
        if not q:
            raise AuthError('Auth data incorrect')

        # TODO we need store token in database for more useful?
        return super(AuthStorage, self).get_token(self)

    # FIXME
    def init_db(self):
        """
        Nothing
        :return:
        """
        pass

    # FIXME
    def remove_db(self):
        """
        Remove user collection
        :return:
        """
        User.drop_collection()

