import unittest
import json
from app import create_app
from config import TestingConfig
from config import MongoTestingConfig
from lib import AuthExtension


class AuthTestCaseSQL(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            self.app.extensions[AuthExtension.ext_name].storage.init_db()

    def test_simple_provider(self):
        # add user
        result = self.client.post('/auth/signup/',
                                  data={'type': 'simple', 'email': 'test@test.ru', 'password': '123331'})
        assert result.status_code == 200

        # duplicate key test
        result = self.client.post('/auth/signup/',
                                  data={'type': 'simple', 'email': 'test@test.ru', 'password': '123331'})
        assert result.status_code == 400

        # add another user
        result = self.client.post('/auth/signup/', data={'type': 'simple', 'email': 'test2@test.ru', 'password': '333'})
        assert result.status_code == 200

        # test signin
        result = self.client.post('/auth/signin/',
                                  data={'type': 'simple', 'email': 'test@test.ru', 'password': '123331'})
        assert result.status_code == 200
        assert 'token' in json.loads(result.data)

        # test wrong signin
        result = self.client.post('/auth/signin/', data={'type': 'simple', 'email': 'test@test.ru', 'password': '1222'})
        assert result.status_code == 400
        assert json.loads(result.data)['message'] == 'Auth data incorrect'
        assert 'token' not in json.loads(result.data)

    def test_facebook_provider(self):
        # add user
        result = self.client.post('/auth/signup/',
                                  data={'type': 'facebook', 'email': 'test@test.ru', 'facebook_id': '1222',
                                        'facebook_token': 'as98asdbas88'})
        assert result.status_code == 200

        # duplicate key test
        result = self.client.post('/auth/signup/',
                                  data={'type': 'facebook', 'email': 'test@test.ru', 'facebook_id': '1222',
                                        'facebook_token': 'as98asdbas88'})
        assert result.status_code == 400

        # add another user
        result = self.client.post('/auth/signup/',
                                  data={'type': 'facebook', 'email': 'test2@test.ru', 'facebook_id': '1445',
                                        'facebook_token': 'as98asdbas99'})
        assert result.status_code == 200

        # test signin
        result = self.client.post('/auth/signin/', data={'type': 'facebook', 'facebook_token': 'as98asdbas88'})
        assert result.status_code == 200
        assert 'token' in json.loads(result.data)

        # test wrong signin
        result = self.client.post('/auth/signin/', data={'type': 'facebook', 'facebook_token': '11111111111'})
        assert result.status_code == 400
        assert json.loads(result.data)['message'] == 'Auth data incorrect'
        assert 'token' not in json.loads(result.data)

    # TODO test instagram provider

    def test_wrong_data_type(self):
        result = self.client.post('/auth/signup/')
        assert result.status_code == 400
        assert json.loads(result.data)['message'] == 'Type not specified'

        result = self.client.post('/auth/signup/', data={'type': 'simple', 'password': '123331'})
        assert result.status_code == 400
        assert json.loads(result.data)['message'] == 'Invalid user data'

    def test_get(self):
        result = self.client.get('/auth/signup/')
        assert result.status_code == 405

    def tearDown(self):
        with self.app.app_context():
            self.app.extensions[AuthExtension.ext_name].storage.remove_db()


class AuthTestCaseMongo(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=MongoTestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            self.app.extensions[AuthExtension.ext_name].storage.init_db()

    def test_simple_provider(self):
        # add user
        result = self.client.post('/auth/signup/',
                                  data={'type': 'simple', 'email': 'test@test.ru', 'password': '123331'})
        assert result.status_code == 200

        # duplicate key test
        result = self.client.post('/auth/signup/',
                                  data={'type': 'simple', 'email': 'test@test.ru', 'password': '123331'})
        assert result.status_code == 400

        # add another user
        result = self.client.post('/auth/signup/', data={'type': 'simple', 'email': 'test2@test.ru', 'password': '333'})
        assert result.status_code == 200

        # test signin
        result = self.client.post('/auth/signin/',
                                  data={'type': 'simple', 'email': 'test@test.ru', 'password': '123331'})
        assert result.status_code == 200

        # test wrong signin
        result = self.client.post('/auth/signin/', data={'type': 'simple', 'email': 'test@test.ru', 'password': '1222'})
        assert result.status_code == 400
        assert json.loads(result.data)['message'] == 'Auth data incorrect'

    def test_facebook_provider(self):
        # add user
        result = self.client.post('/auth/signup/',
                                  data={'type': 'facebook', 'email': 'test@test.ru', 'facebook_id': '1222',
                                        'facebook_token': 'as98asdbas88'})
        assert result.status_code == 200

        # duplicate key test
        result = self.client.post('/auth/signup/',
                                  data={'type': 'facebook', 'email': 'test@test.ru', 'facebook_id': '1222',
                                        'facebook_token': 'as98asdbas88'})
        assert result.status_code == 400

        # add another user
        result = self.client.post('/auth/signup/',
                                  data={'type': 'facebook', 'email': 'test2@test.ru', 'facebook_id': '1445',
                                        'facebook_token': 'as98asdbas99'})
        assert result.status_code == 200

        # test signin
        result = self.client.post('/auth/signin/', data={'type': 'facebook', 'facebook_token': 'as98asdbas88'})
        assert result.status_code == 200

        # test wrong signin
        result = self.client.post('/auth/signin/', data={'type': 'facebook', 'facebook_token': '11111111111'})
        assert result.status_code == 400
        assert json.loads(result.data)['message'] == 'Auth data incorrect'

    # TODO test instagram provider

    def test_wrong_data_type(self):
        result = self.client.post('/auth/signup/')
        assert result.status_code == 400
        assert json.loads(result.data)['message'] == 'Type not specified'

        result = self.client.post('/auth/signup/', data={'type': 'simple', 'password': '123331'})
        assert result.status_code == 400
        assert json.loads(result.data)['message'] == 'Invalid user data'

    def test_get(self):
        result = self.client.get('/auth/signup/')
        assert result.status_code == 405

    def tearDown(self):
        with self.app.app_context():
            self.app.extensions[AuthExtension.ext_name].storage.remove_db()


if __name__ == '__main__':
    unittest.main()
