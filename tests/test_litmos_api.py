from collections import OrderedDict
from requests import HTTPError
from unittest.mock import patch, Mock

from nose.tools import eq_, assert_true, raises

from litmos.api import API


class TestLitmosAPI:
    @classmethod
    def setUpClass(cls):
        API.api_key = 'api-key-123'
        API.app_name = 'app-name-123'

    def test_root_url(self):
        eq_(API.ROOT_URL, 'https://api.litmos.com/v1.svc/')

    @patch('litmos.api.requests.request')
    def test_all(self, request):
        request.side_effect = [
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

    @patch('litmos.api.requests.request')
    def test_get_single_resource(self, request):
        request.return_value = Mock(
            status_code=200,
            text='{\"Id\":\"znJcFwQqfWc2\",\"UserName\":\"john.smith@pieshop.net\"}'
        )

        eq_(API().find('pies', '345'), {'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwQqfWc2'})
        request.assert_called_once_with(
            'GET',
            'https://api.litmos.com/v1.svc/pies/345?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.request')
    def test_create(self, request):
        request.return_value = Mock(
            status_code=200,
            text='[]'
        )

        eq_(API.create('pies', {'Name': 'Cheese & Onion'}), [])
        request.assert_called_once_with(
            'POST',
            'https://api.litmos.com/v1.svc/pies?apikey=api-key-123&source=app-name-123&format=json',
            json={'Name': 'Cheese & Onion'}
        )

    @patch('litmos.api.requests.request')
    def test_update(self, request):
        request.return_value = Mock(
            status_code=200,
            text='[]'
        )

        eq_(API.update('pies', '12345', {'Name': 'Cheese & Onion'}), [])
        request.assert_called_once_with(
            'PUT',
            'https://api.litmos.com/v1.svc/pies/12345?apikey=api-key-123&source=app-name-123&format=json',
            json={'Name': 'Cheese & Onion'}
        )

    @patch('litmos.api.requests.request')
    def test_update_sub_resource(self, request):
        request.return_value = Mock(
            status_code=200,
            text='[]'
        )

        eq_(API.update_sub_resource('pies', None, 'chips', 'five', {'Name': 'Cheese & Onion'}), [])
        request.assert_called_once_with(
            'PUT',
            'https://api.litmos.com/v1.svc/pies/chips/five?apikey=api-key-123&source=app-name-123&format=json',
            json={'Name': 'Cheese & Onion'}
        )

    @patch('litmos.api.requests.request')
    def test_search(self, request):
        request.return_value = Mock(
            status_code=200,
            text='[{\"Id\":\"znJcFwQqfWc2\",\"UserName\":\"john.smith@pieshop.net\"}]'
        )

        eq_(API.search('pies', 'farqhuar'), [{'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwQqfWc2'}])
        request.assert_called_once_with(
            'GET',
            'https://api.litmos.com/v1.svc/pies?apikey=api-key-123&source=app-name-123&format=json&search=farqhuar'
        )

    @patch('litmos.api.requests.request')
    def test_delete(self, request):
        request.return_value = Mock(
            status_code=200,
            text=''
        )

        assert_true(API.delete('pies', 'wsGty'))
        request.assert_called_once_with(
            'DELETE',
            'https://api.litmos.com/v1.svc/pies/wsGty?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.request')
    def test_delete_sub_resource(self, request):
        request.return_value = Mock(
            status_code=200,
            text=''
        )

        assert_true(API.remove_sub_resource('pies', 'wsGty', 'eaters', 'ws2123'))
        request.assert_called_once_with(
            'DELETE',
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters/ws2123?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.request')
    def test_get_sub_resource(self, request):
        request.return_value = Mock(
            status_code=200,
            text='[{\"Id\": \"fgUr3\", \"Name\": \"Charlie\"},{\"Id\": \"fgUr2\", \"Name\": \"John\"}]'
        )

        eq_(
            API.get_sub_resource('pies', 'wsGty', 'eaters'),
            [
                {'Id': 'fgUr3', 'Name': 'Charlie'},
                {'Id': 'fgUr2', 'Name': 'John'}
            ]
        )
        request.assert_called_once_with(
            'GET',
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.api.requests.request')
    def test_add_sub_resource(self, request):
        request.return_value = Mock(
            status_code=201,
            text='{\"Id\": \"1234rf\", \"Name\": \"Charlie\"}'
        )

        eq_(
            API.add_sub_resource('pies', 'wsGty', 'eaters', {'Id': '', 'Name': 'Charlie'}),
            {'Id': '1234rf', 'Name': 'Charlie'}
        )
        request.assert_called_once_with(
            'POST',
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json',
            json={'Id': '', 'Name': 'Charlie'}
        )

    @patch('litmos.api.requests.request')
    def test_perform_request(self, request):
        request.return_value = Mock(
            status_code=200,
            text=''
        )

        API._perform_request(
            'POST',
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json',
            json={'Id': '', 'Name': 'Charlie'}
        )

        request.assert_called_once_with(
            'POST',
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json',
            json={'Id': '', 'Name': 'Charlie'}
        )

    @raises(HTTPError)
    @patch('litmos.api.requests.request')
    def test_perform_request_bad_response(self, request):
        response_mock = Mock()
        response_mock.raise_for_status.side_effect = HTTPError()

        request.return_value = response_mock

        API._perform_request(
            'POST',
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json',
            json={'Id': '', 'Name': 'Charlie'}
        )

        request.assert_called_once_with(
            'POST',
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json',
            json={'Id': '', 'Name': 'Charlie'}
        )

    @patch('litmos.api.requests.request')
    def test_add_sub_resource_list(self, request):
        request.return_value = Mock(
            status_code=201,
            text=''
        )

        result = API.add_sub_resource(
            'pies',
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

        request.assert_called_once_with(
            'POST',
            'https://api.litmos.com/v1.svc/pies/wsGty/eaters?apikey=api-key-123&source=app-name-123&format=json',
            json=[
                OrderedDict([('Id', 'wser4351'),
                             ('UserName', 'paul.smith1'),
                             ('FirstName', 'Paul1'),
                             ('LastName', 'Smith1')]),
                OrderedDict([('Id', 'wser435'),
                             ('UserName', 'paul.smith'),
                             ('FirstName', 'Paul'),
                             ('LastName', 'Smith')])
            ]
        )
