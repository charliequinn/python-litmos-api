from collections import OrderedDict
from unittest.mock import patch

from nose.tools import assert_true, eq_, assert_false

from litmos import LitmosType


class TestLitmosType:
    def test_init_empty_attributes(self):
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema

        user = LitmosType()

        assert_true(hasattr(user, 'Id'))
        assert_true(hasattr(user, 'Name'))

    def test_init(self):
        user = LitmosType({'UserName': 'paul.smith', 'FirstName': 'Paul'})

        assert_true(isinstance(user, LitmosType))
        eq_(user.UserName, 'paul.smith')
        eq_(user.FirstName, 'Paul')

    def test_name(self):
        eq_(LitmosType.name(), 'litmostypes')

    def test_new_record_Id_None(self):
        lm = LitmosType()

        assert_true(lm.is_new_record)

    def test_new_record_Id_Not_None(self):
        lm = LitmosType()
        lm.Id = 'wsQa'

        assert_false(lm.is_new_record)

    @patch('litmos.litmos.API')
    def test_create(self, api_mock):
        api_mock.create.return_value = {"Id": 'ws5tghd', "Name": "Paul"}
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema

        lm = LitmosType.create({'Name': 'Paul'})

        api_mock.create.assert_called_once_with('litmostypes', OrderedDict([('Id', ''), ('Name', 'Paul')]))
        assert_true(isinstance(lm, LitmosType))
        eq_(lm.Id, 'ws5tghd')
        eq_(lm.Name, 'Paul')

    @patch('litmos.litmos.API')
    def test_save(self, api_mock):
        api_mock.update.return_value = None
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema
        lm = LitmosType({'Id': 'wsGty', 'Name': 'Paul'})
        lm.Name = 'James'

        lm.save()

        api_mock.update.assert_called_once_with(
            'litmostypes',
            'wsGty',
            OrderedDict([('Id', 'wsGty'), ('Name', 'James')])
        )
        assert_true(isinstance(lm, LitmosType))
        eq_(lm.Id, 'wsGty')
        eq_(lm.Name, 'James')

    @patch('litmos.litmos.API')
    def test_save_new_record(self, api_mock):
        api_mock.create.return_value = {"Id": 'wsGty123', "Name": "James"}
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema
        lm = LitmosType()
        lm.Name = 'James123'

        lm.save()

        api_mock.create.assert_called_once_with('litmostypes', OrderedDict([('Id', ''), ('Name', 'James123')]))
        assert_true(isinstance(lm, LitmosType))
        eq_(lm.Name, 'James')

    @patch('litmos.litmos.API')
    def test_destroy(self, api_mock):
        api_mock.delete.return_value = True
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema
        lm = LitmosType()
        lm.Id = 'wsDe4123'

        assert_true(lm.destroy())

        api_mock.delete.assert_called_once_with('litmostypes', resource_id=lm.Id)

    @patch('litmos.litmos.API')
    def test_delete(self, api_mock):
        api_mock.delete.return_value = True

        assert_true(LitmosType.delete('wsGty'))

        api_mock.delete.assert_called_once_with('litmostypes', resource_id='wsGty')

    @patch('litmos.litmos.API')
    def test_find(self, api_mock):
        api_mock.find.return_value = {"Id": 'ws5tghd', "Name": "Paul"}
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema

        lm = LitmosType.find('ws5tghd')

        api_mock.find.assert_called_once_with('litmostypes', 'ws5tghd')
        assert_true(isinstance(lm, LitmosType))
        eq_(lm.Id, 'ws5tghd')
        eq_(lm.Name, 'Paul')

    @patch('litmos.litmos.API')
    def test_all(self, api_mock):
        api_mock.all.return_value = [{"Id": 'ws5tghd', "Name": "Paul"}]
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema

        lm_types = LitmosType.all()

        api_mock.all.assert_called_once_with('litmostypes')
        assert_true(isinstance(lm_types[0], LitmosType))
        eq_(lm_types[0].Id, 'ws5tghd')
        eq_(lm_types[0].Name, 'Paul')

    @patch('litmos.litmos.API')
    def test_search(self, api_mock):
        api_mock.search.return_value = [{"Id": 'ws5tghd', "Name": "Paul"}]
        dummy_schema = OrderedDict([('Id', ''),('Name', '')])
        LitmosType.SCHEMA = dummy_schema

        lm_types = LitmosType.search('Paul')

        api_mock.search.assert_called_once_with('litmostypes', 'Paul')
        assert_true(isinstance(lm_types[0], LitmosType))
        eq_(lm_types[0].Id, 'ws5tghd')
        eq_(lm_types[0].Name, 'Paul')
