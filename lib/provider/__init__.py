from abc import abstractmethod, abstractproperty


class BaseUser(object):
    @abstractmethod
    def __init__(self, **entries):
        self.email = None
        self.__dict__.update(entries)

    @abstractmethod
    def is_valid(self):
        return False

    @abstractproperty
    def auth_code(self):
        return None

    @abstractproperty
    def provider(self):
        return None

    @abstractproperty
    def extra_data(self):
        return None


class UserBuilder(object):
    def __init__(self, types):
        self.providers = {}
        for t in types:
            module = __import__(__name__ + '.' + t, fromlist=['User'])
            self.providers[t] = module.User

        pass

    def build(self, user_type, user_data):
        if user_type in self.providers:
            return self.providers[user_type](**user_data)
