import vcr
from datetime import datetime, timedelta
from nose.tools import eq_, assert_true, assert_false

from litmos import Litmos
from litmos.team import Team
from litmos.user import User


class TestLitmosIntegration:
    def setUp(self):
        self.lms = Litmos('app-key12345', 'app-name12345')

    @vcr.use_cassette('fixtures/end-to-end-integration-test.yml')
    def test_end_to_end_showcase(self):
        user1 = self.lms.User.search('jobaba66@pieshop.net')[0]

        user2 = self.lms.User.create({
            'UserName': 'jobaba72@pieshop.net',
            'FirstName': 'Jo',
            'LastName': 'Baba72',
            'Email': 'jobaba72@pieshop.net'
        })

        team = self.lms.Team.create({
            'Name': 'jobaba66',
            'Description': 'Jobaba\'s B team'
        })

        subteam = self.lms.Team()

        subteam.Name = 'jobaba33'
        subteam.Description = 'Jobaba\'s C team'
        subteam.Id = team.add_sub_team(subteam)

        subteam1 = self.lms.Team()

        subteam1.Name = 'jobaba001'
        subteam1.Description = 'Jobaba\'s D team'

        subteam2 = self.lms.Team()

        subteam2.Name = 'jobaba002'
        subteam2.Description = 'Jobaba\'s E team'

        subteam1.Id = subteam.add_sub_team(subteam1)
        subteam2.Id = subteam.add_sub_team(subteam2)

        subteam2.add_users([user1, user2])
        subteam2.promote_team_leader(user1)

        subteam1.add_users([user2, user1])
        subteam1.promote_team_leader(user1)
        subteam1.promote_team_leader(user2)

        subteam1.demote_team_leader(user1)

    @vcr.use_cassette('fixtures/users-all-paginated.yml')
    def test_User_all(self):
        users = self.lms.User.all()

        eq_(len(users), 10)

    @vcr.use_cassette('fixtures/teams-all-paginated.yml')
    def test_Team_all(self):
        teams = self.lms.Team.all()

        eq_(len(teams), 8)

    @vcr.use_cassette('fixtures/users-create.yml')
    def test_User_create(self):
        user = self.lms.User.create({
            'UserName': 'jobaba@pieshop.net',
            'FirstName': 'Jo',
            'LastName': 'Baba',
            'Email': 'jobaba@pieshop.net'
        })

        eq_(user.UserName,'jobaba@pieshop.net')
        eq_(user.FirstName, 'Jo')
        eq_(user.Id, 'ZUhjzXUqmTo1')

    @vcr.use_cassette('fixtures/teams-create.yml')
    def test_Team_create(self):
        team = self.lms.Team.create({
            'Name': 'jobaba',
            'Description': 'Jobaba\'s A team'
        })

        eq_(team.Name,'jobaba')
        eq_(team.Description, 'Jobaba\'s A team')
        eq_(team.Id, 'lFRn-Vl4A941')

    @vcr.use_cassette('fixtures/search-users.yml')
    def test_User_search(self):
        users = self.lms.User.search('charlie.smith@pieshop.net')
        first_user = users[0]

        eq_(len(users), 1)

        eq_(first_user.Active, True)
        eq_(first_user.FirstName, 'Charlie')
        eq_(first_user.LastName, 'Smith')
        eq_(first_user.Id, 'CCzIpPA13Wo1')
        eq_(first_user.UserName, 'charlie.smith@pieshop.net')
        eq_(first_user.AccessLevel, 'Account_Owner')
        eq_(first_user.Email, 'charlie.smith@pieshop.net')

    @vcr.use_cassette('fixtures/delete-user.yml')
    def test_User_delete(self):
        assert_true(self.lms.User.delete('YmrD13iZlm41'))

    @vcr.use_cassette('fixtures/search-users-not-found.yml')
    def test_User_search_not_found(self):
        users = self.lms.User.search('beelzebub@pieshop.net')

        eq_(len(users), 0)

    @vcr.use_cassette('fixtures/find-user.yml')
    def test_User_find(self):
        user = self.lms.User.find('rnjx2WaQOEY1')

        eq_(user.Active, True)
        eq_(user.FirstName, 'Janine')
        eq_(user.LastName, 'Butcher')
        eq_(user.Id, 'rnjx2WaQOEY1')
        eq_(user.UserName, 'janine.butcher@pieshop.net')
        eq_(user.AccessLevel, 'Learner')
        eq_(user.Email, 'janine.butcher@pieshop.net')

    @vcr.use_cassette('fixtures/find-and-update-user.yml')
    def test_User_update(self):
        user = self.lms.User.search('charlie.quinn')[0]

        user.Skype = 'skypeeeeeewoo'

        assert_true(user.save())

    @vcr.use_cassette('fixtures/create-new-user.yml')
    def test_User_create_new(self):
        user = self.lms.User()

        user.UserName = 'charlie.quinn123@pieshop.net'
        user.Email = 'charlie.quinn123@pieshop.net'
        user.FirstName = 'Charlie'
        user.LastName = 'Quinn'

        assert_true(user.save())
        eq_('-yJ1NfrpHz41', user.Id)

    @vcr.use_cassette('fixtures/deactivate-user.yml')
    def test_User_deactivate(self):
        user = self.lms.User.search('paul.smith2')[0]

        assert_true(user.Active)

        user.Active = False
        assert_true(user.save())

        user = self.lms.User.search('paul.smith2')[0]
        assert_false(user.Active)

    @vcr.use_cassette('fixtures/get-sub-teams.yml')
    def test_get_subteams(self):
        team = self.lms.Team.find('JyLa085jwVs1')

        teams = team.sub_teams()

        assert_true(isinstance(teams[0], Team))
        eq_(len(teams), 2)

    @vcr.use_cassette('fixtures/get-team-users.yml')
    def test_get_users(self):
        team = self.lms.Team.find('JyLa085jwVs1')

        users = team.users()

        assert_true(isinstance(users[0], User))
        eq_(len(users), 3)

    @vcr.use_cassette('fixtures/add-sub-team.yml')
    def test_add_sub_team(self):
        team = self.lms.Team.find('JyLa085jwVs1')

        sub_team = self.lms.Team()
        sub_team.Name = 'Bob\'s A-Team'
        sub_team.Description = 'Make Pies Great Again'

        sub_team_id = team.add_sub_team(sub_team)

        eq_(sub_team_id, 'L4NTbLzz7rI1')

    @vcr.use_cassette('fixtures/add-users.yml')
    def test_add_users(self):
        team = self.lms.Team.find('JyLa085jwVs1')

        team_member1 = self.lms.User.create({
            'UserName': 'jobaba1@pieshop.net',
            'FirstName': 'Jo',
            'LastName': 'Baba1',
            'Email': 'jobaba1@pieshop.net'
        })

        team_member2 = self.lms.User.create({
            'UserName': 'jobaba2@pieshop.net',
            'FirstName': 'Jo',
            'LastName': 'Baba2',
            'Email': 'jobaba2@pieshop.net'
        })

        assert_true(
            team.add_users([team_member1,
                            team_member2])
        )

    @vcr.use_cassette('fixtures/remove-user.yml')
    def test_remove_user(self):
        team = self.lms.Team.find('JyLa085jwVs1')

        team_member1 = self.lms.User.create({
            'UserName': 'jobaba7@pieshop.net',
            'FirstName': 'Jo',
            'LastName': 'Baba7',
            'Email': 'jobaba7@pieshop.net'
        })

        team.add_users([team_member1])

        assert_true(team.remove_user(team_member1))

    @vcr.use_cassette('fixtures/remove-teams-from-user.yml')
    def test_remove_teams_from_user(self):
        user = self.lms.User.search('jobaba2@pieshop.net')[0]

        assert_true(user.remove_teams())

    @vcr.use_cassette('fixtures/promote-and-demote-user.yml')
    def test_promote_and_demote(self):
        team = self.lms.Team.find('JyLa085jwVs1')

        team_member1 = self.lms.User.create({
            'UserName': 'jobaba100@pieshop.net',
            'FirstName': 'Jo',
            'LastName': 'Baba100',
            'Email': 'jobaba100@pieshop.net'
        })

        team_member2 = self.lms.User.create({
            'UserName': 'jobaba66@pieshop.net',
            'FirstName': 'Jo',
            'LastName': 'Baba66',
            'Email': 'jobaba66@pieshop.net'
        })

        team.add_users([team_member1, team_member2])

        team.promote_team_leader(team_member1)
        assert_true(team.demote_team_leader(team_member1))

    @vcr.use_cassette('fixtures/mark-module-complete.yml')
    def test_course_module_complete(self):
        course = self.lms.Course.find('RuzXNaD42Sw1')

        modules = course.modules()

        team_member1 = self.lms.User.find('CCzIpPA8OWo1')

        attributes = {
            'UserId': team_member1.Id,
            'Score': 100,
            'Completed': True,
            'UpdatedAt': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'Note': ''
        }

        assert_true(course.module_complete(modules[0].Id, attributes))
