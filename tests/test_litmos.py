from collections import OrderedDict
from unittest.mock import patch, Mock

from nose.tools import raises, assert_true, eq_

from litmos.litmos import Litmos, LitmosAPI, LitmosType


class TestLitmos:
    def test_acceptable_types(self):
        eq_(Litmos.ACCEPTABLE_TYPES, ['User', 'Team'])

    def test_init(self):
        litmos = Litmos('app-key-123456', 'app-name-123456')

        eq_(litmos.litmos_api, LitmosAPI)

    def test_User(self):
        litmos = Litmos('app-key-123456', 'app-name-123456')
        user = litmos.User

        eq_(user.__name__, 'User')

    @raises(AttributeError)
    def test_non_acceptable_types(self):
        litmos = Litmos('app-key-123456', 'app-name-123456')
        litmos.Pie


class TestLitmosAPI:
    def test_root_url(self):
        eq_(LitmosAPI.ROOT_URL,'https://api.litmos.com/v1.svc/')

    @patch('litmos.litmos.requests.get')
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

        LitmosAPI.api_key = 'api-key-123'
        LitmosAPI.app_name = 'app-name-123'

        eq_(LitmosAPI().all('pies'),
            [{'UserName': 'john.clark@pieshop.net', 'Id': 'znJcFaXqfWc2'},
             {'UserName': 'john.kent@pieshop.net', 'Id': 'znJcFtPqfWc2'},
             {'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwLlfWc2'}])

    @patch('litmos.litmos.requests.get')
    def test_find_not_found(self, requests_get):
        requests_get.return_value = Mock(status_code=404, text='Not found')

        LitmosAPI.api_key = 'api-key-123'
        LitmosAPI.app_name = 'app-name-123'

        eq_(LitmosAPI().find('pies', '123'), None)
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/123?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.litmos.requests.get')
    def test_get_single_resource(self, requests_get):
        requests_get.return_value = Mock(
            status_code=200,
            text='{\"Id\":\"znJcFwQqfWc2\",\"UserName\":\"john.smith@pieshop.net\"}'
        )

        LitmosAPI.api_key = 'api-key-123'
        LitmosAPI.app_name = 'app-name-123'

        eq_(LitmosAPI().find('pies', '345'), {'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwQqfWc2'})
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/345?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.litmos.requests.post')
    def test_create(self, requests_post):
        requests_post.return_value = Mock(
            status_code=200,
            text='[]'
        )

        LitmosAPI.api_key = 'api-key-123'
        LitmosAPI.app_name = 'app-name-123'

        eq_(LitmosAPI().create('pies', {'Name': 'Cheese & Onion'}), [])
        requests_post.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies?apikey=api-key-123&source=app-name-123&format=json',
            json={'Name': 'Cheese & Onion'}
        )

    @patch('litmos.litmos.requests.get')
    def test_search(self, requests_get):
        requests_get.return_value = Mock(
            status_code=200,
            text='[{\"Id\":\"znJcFwQqfWc2\",\"UserName\":\"john.smith@pieshop.net\"}]'
        )

        LitmosAPI.api_key = 'api-key-123'
        LitmosAPI.app_name = 'app-name-123'

        eq_(LitmosAPI().search('pies', 'farqhuar'), [{'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwQqfWc2'}])
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies?apikey=api-key-123&source=app-name-123&format=json&search=farqhuar'
        )


class TestLitmosType:
    def test_init(self):
        user = LitmosType({'UserName': 'paul.smith', 'FirstName': 'Paul'})

        assert_true(isinstance(user, LitmosType))
        eq_(user.UserName, 'paul.smith')
        eq_(user.FirstName, 'Paul')

    def test_name(self):
        eq_(LitmosType.name(), 'litmostypes')

    @patch('litmos.litmos.LitmosAPI')
    def test_create(self, api_mock):
        api_mock.create.return_value = {"Id": 'ws5tghd', "Name": "Paul"}
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema

        lm = LitmosType.create({'Name': 'Paul'})

        api_mock.create.assert_called_once_with('litmostypes', OrderedDict([('Id', ''), ('Name', 'Paul')]))
        assert_true(isinstance(lm, LitmosType))
        eq_(lm.Id, 'ws5tghd')
        eq_(lm.Name, 'Paul')

    @patch('litmos.litmos.LitmosAPI')
    def test_find(self, api_mock):
        api_mock.find.return_value = {"Id": 'ws5tghd', "Name": "Paul"}
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema

        lm = LitmosType.find('ws5tghd')

        api_mock.find.assert_called_once_with('litmostypes', 'ws5tghd')
        assert_true(isinstance(lm, LitmosType))
        eq_(lm.Id, 'ws5tghd')
        eq_(lm.Name, 'Paul')

    @patch('litmos.litmos.LitmosAPI')
    def test_all(self, api_mock):
        api_mock.all.return_value = [{"Id": 'ws5tghd', "Name": "Paul"}]
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema

        lm_types = LitmosType.all()

        api_mock.all.assert_called_once_with('litmostypes')
        assert_true(isinstance(lm_types[0], LitmosType))
        eq_(lm_types[0].Id, 'ws5tghd')
        eq_(lm_types[0].Name, 'Paul')

    @patch('litmos.litmos.LitmosAPI')
    def test_search(self, api_mock):
        api_mock.search.return_value = [{"Id": 'ws5tghd', "Name": "Paul"}]
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema

        lm_types = LitmosType.search('Paul')

        api_mock.search.assert_called_once_with('litmostypes', 'Paul')
        assert_true(isinstance(lm_types[0], LitmosType))
        eq_(lm_types[0].Id, 'ws5tghd')
        eq_(lm_types[0].Name, 'Paul')
