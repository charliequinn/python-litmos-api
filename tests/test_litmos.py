from collections import OrderedDict
from unittest.mock import patch

from nose.tools import raises, assert_true, assert_false, eq_

from litmos.litmos import Litmos, LitmosType, User, Team
from litmos.api import API


class TestLitmos:
    def test_acceptable_types(self):
        eq_(Litmos.ACCEPTABLE_TYPES, ['User', 'Team'])

    def test_init(self):
        litmos = Litmos('app-key-123456', 'app-name-123456')

        eq_(litmos.litmos_api, API)

    def test_User(self):
        litmos = Litmos('app-key-123456', 'app-name-123456')
        user = litmos.User

        eq_(user.__name__, 'User')

    @raises(AttributeError)
    def test_non_acceptable_types(self):
        litmos = Litmos('app-key-123456', 'app-name-123456')
        litmos.Pie


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

        api_mock.update.assert_called_once_with('litmostypes', 'wsGty', OrderedDict([('Id', 'wsGty'), ('Name', 'James')]))
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


class TestUser:
    @patch('litmos.litmos.API')
    def test_deactivate(self, api_mock):
        api_mock.update.return_value = True

        user = User({'Id': 'wsGth', 'Active': True})

        assert_true(user.deactivate())

        api_mock.update.assert_called_once_with('users', 'wsGth', OrderedDict([('Id', 'wsGth'), ('UserName', ''), ('FirstName', ''), ('LastName', ''), ('FullName', ''), ('Email', ''), ('AccessLevel', 'Learner'), ('DisableMessages', True), ('Active', False), ('Skype', ''), ('PhoneWork', ''), ('PhoneMobile', ''), ('LastLogin', ''), ('LoginKey', ''), ('IsCustomUsername', False), ('Password', ''), ('SkipFirstLogin', True), ('TimeZone', 'UTC'), ('Street1', ''), ('Street2', ''), ('City', ''), ('State', ''), ('PostalCode', ''), ('Country', ''), ('CompanyName', ''), ('JobTitle', ''), ('CustomField1', ''), ('CustomField2', ''), ('CustomField4', ''), ('CustomField5', ''), ('CustomField6', ''), ('CustomField7', ''), ('CustomField8', ''), ('CustomField9', ''), ('CustomField10', ''), ('Culture', '')]))

    @patch('litmos.litmos.API')
    def test_remove_teams(self, api_mock):
        api_mock.remove_sub_resource.return_value = True

        user = User({'Id': 'fgUr2', 'Name': 'User1'})

        assert_true(user.remove_teams())

        api_mock.remove_sub_resource.assert_called_once_with('users',
                                                             user.Id,
                                                             'teams',
                                                             None)


class TestTeam:
    @patch('litmos.litmos.API')
    def test_subteams(self, api_mock):
        api_mock.get_sub_resource.return_value = [
            {'Id': 'fgUr3', 'Name': 'SubTeam1'},
            {'Id': 'fgUr2', 'Name': 'SubTeam2'}
        ]

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        subteams = team.sub_teams()

        eq_(2, len(subteams))
        api_mock.get_sub_resource.assert_called_once_with('teams', 'fgUr1', 'teams')

    @patch('litmos.litmos.API')
    def test_users(self, api_mock):
        api_mock.get_sub_resource.return_value = [
            {'Id': 'fgUr3', 'Name': 'SubTeam1'},
            {'Id': 'fgUr2', 'Name': 'SubTeam2'}
        ]

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        users = team.users()

        eq_(len(users), 2)
        eq_('fgUr3', users[0].Id)

        api_mock.get_sub_resource.assert_called_once_with('teams', 'fgUr1', 'users')

    @patch('litmos.litmos.API')
    def test_leaders(self, api_mock):
        api_mock.get_sub_resource.return_value = [
            {'Id': 'fgUr3', 'Name': 'TeamLeader1'},
        ]

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        users = team.leaders()

        eq_(len(users), 1)
        eq_('fgUr3', users[0].Id)
        assert_true(isinstance(users[0], User))

        api_mock.get_sub_resource.assert_called_once_with('teams', 'fgUr1', 'leaders')

    @patch('litmos.litmos.API')
    def test_add_sub_team(self, api_mock):
        api_mock.add_sub_resource.return_value = {'Id':'wsd456Yh', 'Name': 'SubTeam1', 'Description': 'SS'}

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        sub_team = Team({'Name': 'SubTeam1'})

        eq_(sub_team.Id, '')

        new_sub_team_id = team.add_sub_team(sub_team)

        eq_(new_sub_team_id, 'wsd456Yh')
        api_mock.add_sub_resource.assert_called_once_with('teams', 'fgUr1', 'teams', OrderedDict([('Id', ''), ('Name', 'SubTeam1'), ('Description', '')]))

    @patch('litmos.litmos.API')
    def test_add_users(self, api_mock):
        api_mock.add_sub_resource.return_value = True

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        user1 = User({'FirstName': 'Paul1', 'LastName': 'Smith1', 'UserName': 'paul.smith1', 'Id': 'wser4351'})
        user2 = User({'FirstName': 'Paul', 'LastName': 'Smith', 'UserName': 'paul.smith', 'Id': 'wser435'})

        assert_true(team.add_users([user1, user2]))

        api_mock.add_sub_resource.assert_called_once_with(
            'teams',
            'fgUr1',
            'users',
            [OrderedDict([('Id', 'wser4351'), ('UserName', 'paul.smith1'), ('FirstName', 'Paul1'), ('LastName', 'Smith1')]),
             OrderedDict([('Id', 'wser435'), ('UserName', 'paul.smith'), ('FirstName', 'Paul'), ('LastName', 'Smith')])]
        )

    @patch('litmos.litmos.API')
    def test_promote_leader(self, api_mock):
        api_mock.update_sub_resource.return_value = True

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        user1 = User({'FirstName': 'Paul1', 'LastName': 'Smith1', 'UserName': 'paul.smith1', 'Id': 'wser4351'})

        assert_true(team.promote_team_leader(user1))

        api_mock.update_sub_resource.assert_called_once_with(
            'teams',
            team.Id,
            'leaders',
            user1.Id
        )

    @patch('litmos.litmos.API')
    def test_demote_leader(self, api_mock):
        api_mock.remove_sub_resource.return_value = True

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        user1 = User({'FirstName': 'Paul1', 'LastName': 'Smith1', 'UserName': 'paul.smith1', 'Id': 'wser4351'})

        assert_true(team.demote_team_leader(user1))

        api_mock.remove_sub_resource.assert_called_once_with(
            'teams',
            team.Id,
            'leaders',
            user1.Id
        )

    @patch('litmos.litmos.API')
    def test_remove_user(self, api_mock):
        api_mock.remove_sub_resource.return_value = True

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})
        user = User({'Id': 'fgUr2', 'Name': 'User1'})

        assert_true(team.remove_user(user))

        api_mock.remove_sub_resource.assert_called_once_with('teams',
                                                             team.Id,
                                                             'users',
                                                             user.Id)
