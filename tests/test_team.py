from collections import OrderedDict
from unittest.mock import patch

from nose.tools import eq_, assert_true

from litmos import Team, User, Course


class TestTeam:
    @patch('litmos.team.API')
    def test_subteams(self, api_mock):
        api_mock.get_sub_resource.return_value = [
            {'Id': 'fgUr3', 'Name': 'SubTeam1'},
            {'Id': 'fgUr2', 'Name': 'SubTeam2'}
        ]

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        subteams = team.sub_teams()

        eq_(2, len(subteams))
        api_mock.get_sub_resource.assert_called_once_with('teams', 'fgUr1', 'teams')

    @patch('litmos.team.API')
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

    @patch('litmos.team.API')
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

    @patch('litmos.team.API')
    def test_admins(self, api_mock):
        api_mock.get_sub_resource.return_value = [
            {'Id': 'fgUr3', 'Name': 'admin2'},
        ]

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        users = team.admins()

        eq_(len(users), 1)
        eq_('fgUr3', users[0].Id)
        assert_true(isinstance(users[0], User))

        api_mock.get_sub_resource.assert_called_once_with('teams', 'fgUr1', 'admins')

    @patch('litmos.team.API')
    def test_courses(self, api_mock):
        api_mock.get_sub_resource.return_value = [
            {'Id': 'fgUr3a', 'Name': 'course1'},
        ]

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        courses = team.courses()

        eq_(len(courses), 1)
        eq_('fgUr3a', courses[0].Id)
        assert_true(isinstance(courses[0], Course))

        api_mock.get_sub_resource.assert_called_once_with('teams', 'fgUr1', 'courses')

    @patch('litmos.team.API')
    def test_add_sub_team(self, api_mock):
        api_mock.add_sub_resource.return_value = {'Id':'wsd456Yh', 'Name': 'SubTeam1', 'Description': 'SS'}

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        sub_team = Team({'Name': 'SubTeam1'})

        eq_(sub_team.Id, '')

        new_sub_team_id = team.add_sub_team(sub_team)

        eq_(new_sub_team_id, 'wsd456Yh')
        api_mock.add_sub_resource.assert_called_once_with(
            'teams',
            'fgUr1',
            'teams',
            OrderedDict([('Id', ''),
                         ('Name', 'SubTeam1'),
                         ('Description', '')]
                        )
        )

    @patch('litmos.team.API')
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
        )

    @patch('litmos.team.API')
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

    @patch('litmos.team.API')
    def test_promote_team_admin(self, api_mock):
        api_mock.update_sub_resource.return_value = True

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        user1 = User({'FirstName': 'Paul1', 'LastName': 'Smith1', 'UserName': 'paul.smith1', 'Id': 'wser4351'})

        assert_true(team.promote_team_admin(user1))

        api_mock.update_sub_resource.assert_called_once_with(
            'teams',
            team.Id,
            'admins',
            user1.Id
        )

    @patch('litmos.team.API')
    def test_demote_team_admin(self, api_mock):
        api_mock.update_sub_resource.return_value = True

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        user1 = User({'FirstName': 'Paul1', 'LastName': 'Smith1', 'UserName': 'paul.smith1', 'Id': 'wser4351'})

        assert_true(team.demote_team_admin(user1))

        api_mock.remove_sub_resource.assert_called_once_with(
            'teams',
            team.Id,
            'admins',
            user1.Id
        )

    @patch('litmos.team.API')
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

    @patch('litmos.team.API')
    def test_remove_user(self, api_mock):
        api_mock.remove_sub_resource.return_value = True

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})
        user = User({'Id': 'fgUr2', 'Name': 'User1'})

        assert_true(team.remove_user(user))

        api_mock.remove_sub_resource.assert_called_once_with(
            'teams',
            team.Id,
            'users',user.Id
        )

    @patch('litmos.team.API')
    def test_assign_courses(self, api_mock):
        api_mock.add_sub_resource.return_value = True

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        course1 = Course({'Id': '1234567890', 'CourseTeamLibrary': ''})
        course2 = Course({'Id': '1234567899', 'CourseTeamLibrary': ''})

        assert_true(team.assign_courses([course1, course2]))

        api_mock.add_sub_resource.assert_called_once_with(
            'teams',
            'fgUr1',
            'courses',
            [
                OrderedDict([('Id', '1234567890'),
                         ('CourseTeamLibrary', '')]),
                OrderedDict([('Id', '1234567899'),
                         ('CourseTeamLibrary', '')])
            ]
        )

    @patch('litmos.team.API')
    def test_unassign_courses(self, api_mock):
        api_mock.remove_sub_resources.return_value = True

        team = Team({'Id': 'fgUr1', 'Name': 'Team1'})

        course1 = Course({'Id': '1234567890', 'CourseTeamLibrary': ''})
        course2 = Course({'Id': '1234567899', 'CourseTeamLibrary': ''})

        assert_true(team.unassign_courses([course1, course2]))

        api_mock.remove_sub_resources.assert_called_once_with(
            'teams',
            'fgUr1',
            'courses',
            [
                OrderedDict([('Id', '1234567890'),
                             ('CourseTeamLibrary', '')]),
                OrderedDict([('Id', '1234567899'),
                             ('CourseTeamLibrary', '')])
            ]
        )


