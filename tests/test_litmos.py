from unittest.mock import patch, Mock

from nose.tools import raises, eq_, assert_true

from litmos.litmos import Payload, Litmos, LitmosType, LitmosAPI


class TestPayload():
    def test_init(self):
        json_dict = {'variable_name_1': 123.4, 'variable_name_4': 'Test'}
        payload = Payload(json_dict)

        eq_(payload.variable_name_1, json_dict['variable_name_1'])
        eq_(payload.variable_name_4, json_dict['variable_name_4'])


class TestLitmos():
    def test_acceptable_types(self):
        eq_(Litmos.ACCEPTABLE_TYPES, ['User', 'Team'])

    def test_init(self):
        litmos = Litmos('app-key-123456', 'app-name-123456')

        assert_true(isinstance(litmos.litmos_api, LitmosAPI))

    def test_User(self):
        litmos = Litmos('app-key-123456', 'app-name-123456')
        user = litmos.User

        eq_(type(user), LitmosType)
        eq_(user.resource_name, 'users')
        eq_(litmos.litmos_api, user.litmos_api)

    @raises(AttributeError)
    def test_non_acceptable_types(self):
        litmos = Litmos('app-key-123456', 'app-name-123456')
        litmos.Pie


class TestLitmosAPI():
    def test_root_url(self):
        eq_(LitmosAPI.ROOT_URL,'https://api.litmos.com/v1.svc/')

    def test_init(self):
        litmos_api = LitmosAPI('api-key-123', 'app-name-123')

        eq_(litmos_api.api_key, 'api-key-123')
        eq_(litmos_api.app_name, 'app-name-123')

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

        litmos_api = LitmosAPI('api-key-123', 'app-name-123')

        eq_(litmos_api.all('pies'),
            [{'UserName': 'john.clark@pieshop.net', 'Id': 'znJcFaXqfWc2'},
             {'UserName': 'john.kent@pieshop.net', 'Id': 'znJcFtPqfWc2'},
             {'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwLlfWc2'}])

    @patch('litmos.litmos.requests.get')
    def test_find_not_found(self, requests_get):
        requests_get.return_value = Mock(status_code=404, text='Not found')

        litmos_api = LitmosAPI('api-key-123', 'app-name-123')

        eq_(litmos_api.find('pies', '123'), None)
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/123?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.litmos.requests.get')
    def test_get_single_resource(self, requests_get):
        requests_get.return_value = Mock(
            status_code=200,
            text='{\"Id\":\"znJcFwQqfWc2\",\"UserName\":\"john.smith@pieshop.net\"}'
        )

        litmos_api = LitmosAPI('api-key-123', 'app-name-123')

        eq_(litmos_api.find('pies', '345'), {'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwQqfWc2'})
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies/345?apikey=api-key-123&source=app-name-123&format=json'
        )

    @patch('litmos.litmos.requests.get')
    def test_search(self, requests_get):
        requests_get.return_value = Mock(
            status_code=200,
            text='[{\"Id\":\"znJcFwQqfWc2\",\"UserName\":\"john.smith@pieshop.net\"}]'
        )

        litmos_api = LitmosAPI('api-key-123', 'app-name-123')

        eq_(litmos_api.search('pies', 'farqhuar'), [{'UserName': 'john.smith@pieshop.net', 'Id': 'znJcFwQqfWc2'}])
        requests_get.assert_called_once_with(
            'https://api.litmos.com/v1.svc/pies?apikey=api-key-123&source=app-name-123&format=json&search=farqhuar'
        )


class TestLitmosType():
    def test_init(self):
        litmos_type = LitmosType('Pie', {'dd': 3})

        eq_(litmos_type.resource_name, 'pies')
        eq_(litmos_type.litmos_api, {'dd': 3})
