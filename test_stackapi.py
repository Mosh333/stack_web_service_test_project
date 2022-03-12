import unittest
from stackapi.application import APPLICATION
from base64 import b64encode


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        APPLICATION.config['TESTING'] = True
        self.app = APPLICATION.test_client()

    def tearDown(self):
        pass

    def auth_header(self, username, password):
        return {
            'Authorization': 'Basic {}'.format(
                b64encode('{}:{}'.format(username, password))),
        }


class HelloTest(BaseTestCase):
    def test_hello_world(self):
        ret = self.app.get('/')
        assert 200 == ret.status_code
        assert 'Hello World' in ret.data


class StackTest(BaseTestCase):
    def test_get_empty_stack(self):
        ret = self.app.get('/stack', headers=self.auth_header(
            APPLICATION.config['HTTP_AUTH_USERNAME'],
            APPLICATION.config['HTTP_AUTH_PASSWORD'])
        )
        assert ret.data, "Stack is not empty!"

if __name__ == '__main__':
    unittest.main()
