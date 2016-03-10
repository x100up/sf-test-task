import uuid


class BaseAuthStorage(object):

    def get_token(self, user):
        """
        :param user: user object
        :type user: auth.provider.BaseUser
        :return:
        :rtype: str or unicode
        """
        return str(uuid.uuid1())