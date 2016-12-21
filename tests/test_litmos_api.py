from collections import OrderedDict
from unittest.mock import patch, Mock

from nose.tools import eq_, assert_true, assert_false

from litmos.api import API


class TestLitmosAPI:
    @classmethod
    def setUpClass(cls):
        API.api_key = 'api-key-123'
        API.app_name = 'app-name-123'

    def test_root_url(self):
        eq_(API.ROOT_URL, 'https://api.litmos.com/v1.svc/')

    @patch('litmos.api.requests.get')
    def test_all(self, requests_get):
        requests_get.side_effect = [
            Mock(
                status_code=200,
                text='[{\"Id\":\"znJcFaXqfWc2\",\"UserName\":\"john.clark@pieshop.net\"}]'
            ),
            Mock(
                status_code=200,
                text='[{\"Id\":\"znJcFtPqfWc2\",\"UserName\":\"john.kent@pieshop.net\"}]'
            ),
            Mock(
                status_code=200,
                text='[{\"Id\":\"znJcFwLlfWc2\",\"UserName\":\"john.smith@pieshop.net\"}]'
            ),
            Mock(
                status_code=200,
                text='[]'
            )
        ]

        eq_(API().all('pies'),
            [{'UserName': 'john.clark@pieshop.net', 'Id': 'znJcFaXqfWc2'},
             {'UserName': 'john.kent@pieshop.net', 'Id': 'znJcFtPqfWc2'},
             {'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwLlfWc2'}])

    @patch('litmos.api.requests.get')
    def test_find_not_found(self, requests_get):
        requests_get.return_value = Mock(status_code=404, text='Not found')

        eq_(API().find('pies', '123'), None)
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/123?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.get')
    def test_get_single_resource(self, requests_get):
        requests_get.return_value = Mock(
            status_code=200,
            text='{\"Id\":\"znJcFwQqfWc2\",\"UserName\":\"john.smith@pieshop.net\"}'
        )

        eq_(API().find('pies', '345'), {'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwQqfWc2'})
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/345?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.post')
    def test_create(self, requests_post):
        requests_post.return_value = Mock(
            status_code=200,
            text='[]'
        )

        eq_(API().create('pies', {'Name': 'Cheese & Onion'}), [])
        requests_post.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies?apikey=api-key-123&source=app-name-123&format=json',
            json={'Name': 'Cheese & Onion'}
        )

    @patch('litmos.api.requests.post')
    def test_create(self, requests_post):
        requests_post.return_value = Mock(
            status_code=200,
            text='[]'
        )

        eq_(API().create('pies', {'Name': 'Cheese & Onion'}), [])
        requests_post.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies?apikey=api-key-123&source=app-name-123&format=json',
            json={'Name': 'Cheese & Onion'}
        )

    @patch('litmos.api.requests.put')
    def test_update(self, requests_put):
        requests_put.return_value = Mock(
            status_code=200,
            text='[]'
        )

        eq_(API().update('pies', '12345', {'Name': 'Cheese & Onion'}), [])
        requests_put.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/12345?apikey=api-key-123&source=app-name-123&format=json',
            json={'Name': 'Cheese & Onion'}
        )

    @patch('litmos.api.requests.get')
    def test_search(self, requests_get):
        requests_get.return_value = Mock(
            status_code=200,
            text='[{\"Id\":\"znJcFwQqfWc2\",\"UserName\":\"john.smith@pieshop.net\"}]'
        )

        eq_(API().search('pies', 'farqhuar'), [{'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwQqfWc2'}])
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies?apikey=api-key-123&source=app-name-123&format=json&search=farqhuar'
        )

    @patch('litmos.api.requests.delete')
    def test_delete(self, requests_delete):
        requests_delete.return_value = Mock(
            status_code=200,
            text=''
        )

        assert_true(API().delete('pies', 'wsGty'))
        requests_delete.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/wsGty?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.delete')
    def test_delete_fail(self, requests_delete):
        requests_delete.return_value = Mock(
            status_code=404,
            text=''
        )

        assert_false(API().delete('pies', 'wsGty'))
        requests_delete.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/wsGty?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.delete')
    def test_delete_sub_resource(self, requests_delete):
        requests_delete.return_value = Mock(
            status_code=200,
            text=''
        )

        assert_true(API.remove_sub_resource('pies', 'wsGty', 'eaters', 'ws2123'))
        requests_delete.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters/ws2123?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.get')
    def test_get_sub_resource(self, requests_get):
        requests_get.return_value = Mock(
            status_code=200,
            text='[{\"Id\": \"fgUr3\", \"Name\": \"Charlie\"},{\"Id\": \"fgUr2\", \"Name\": \"John\"}]'
        )

        eq_(
            API().get_sub_resource('pies', 'wsGty', 'eaters'),
            [
                {'Id': 'fgUr3', 'Name': 'Charlie'},
                {'Id': 'fgUr2', 'Name': 'John'}
            ]
        )
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.post')
    def test_add_sub_resource(self, requests_post):
        requests_post.return_value = Mock(
            status_code=201,
            text='{\"Id\": \"1234rf\", \"Name\": \"Charlie\"}'
        )

        eq_(
            API.add_sub_resource('pies', 'wsGty', 'eaters', {'Id': '', 'Name': 'Charlie'}),
            {'Id': '1234rf', 'Name': 'Charlie'}
        )
        requests_post.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json',
            json={'Id': '', 'Name': 'Charlie'}
        )

    @patch('litmos.api.requests.post')
    def test_add_sub_resource_list(self, requests_post):
        requests_post.return_value = Mock(
            status_code=201,
            text=''
        )

        result = API.add_sub_resource('pies',
                                 'wsGty',
                                 'eaters',
                                 [
                                    OrderedDict([('Id', 'wser4351'),
                                                 ('UserName', 'paul.smith1'),
                                                 ('FirstName', 'Paul1'),
                                                 ('LastName', 'Smith1')]),
                                    OrderedDict([('Id', 'wser435'),
                                                 ('UserName', 'paul.smith'),
                                                 ('FirstName', 'Paul'),
                                                 ('LastName', 'Smith')])
                                 ]
                                 ),

        assert_true(result)
        requests_post.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json',
            json=[OrderedDict([('Id', 'wser4351'), ('UserName', 'paul.smith1'), ('FirstName', 'Paul1'), ('LastName', 'Smith1')]), OrderedDict([('Id', 'wser435'), ('UserName', 'paul.smith'), ('FirstName', 'Paul'), ('LastName', 'Smith')])]
        )
