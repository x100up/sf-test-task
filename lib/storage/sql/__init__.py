from sqlalchemy import Column, Integer, String, UniqueConstraint, Table, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from lib import AuthError
from lib.storage import BaseAuthStorage

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (UniqueConstraint('email', 'provider', name='user_email_provider_uc'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    auth_code = Column(String, unique=True)
    data = Column(String)


class AuthStorage(BaseAuthStorage):
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.sessionmaker = sessionmaker(bind=self.engine)

    def save_user(self, user):
        """
        Save user to database
        :param user: user object
        :type user: auth.provider.BaseUser
        """
        db_user = User(email=user.email, provider=user.provider, auth_code=user.auth_code, data=user.extra_data)
        session = self.sessionmaker()
        session.add(db_user)
        session.commit()
        session.close()

    def get_token(self, user):
        """
        :param user: user object
        :type user: lib.provider.BaseUser
        :return:
        :rtype: str or unicode
        """
        session = self.sessionmaker()
        try:
            session.query(User).filter(User.auth_code == user.auth_code, User.provider == user.provider).one()
        except NoResultFound:
            raise AuthError('Auth data incorrect')

        # TODO we need store token in database for more useful?
        return super(AuthStorage, self).get_token(self)


    # FIXME
    def init_db(self):
        """
        Create data schema.
        :return:
        """
        metadata.create_all(self.engine)

    # FIXME
    def remove_db(self):
        """
        Remove data schema.
        :return:
        """
        metadata.drop_all(self.engine)

