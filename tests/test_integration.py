from nose.tools import eq_
import vcr

from litmos.litmos import Litmos


class TestLitmosIntegration():
    @vcr.use_cassette('fixtures/users-all-paginated.yml')
    def test_User_all(self):
        lms = Litmos('app-key1234', 'app-name12345')

        users = lms.User.all()

        eq_(len(users), 10)

    @vcr.use_cassette('fixtures/teams-all-paginated.yml')
    def test_Team_all(self):
        lms = Litmos('app-key1234', 'app-name12345')

        teams = lms.Team.all()

        eq_(len(teams), 8)

    @vcr.use_cassette('fixtures/search-users.yml')
    def test_User_search(self):
        lms = Litmos('app-key12345', 'app-name12345')

        users = lms.User.search('charlie.smith@pieshop.net')
        first_user = users[0]

        eq_(len(users), 1)

        eq_(first_user.Active, True)
        eq_(first_user.FirstName, 'Charlie')
        eq_(first_user.LastName, 'Smith')
        eq_(first_user.Id, 'CCzIpPA13Wo1')
        eq_(first_user.UserName, 'charlie.smith@pieshop.net')
        eq_(first_user.AccessLevel, 'Account_Owner')
        eq_(first_user.Email, 'charlie.smith@pieshop.net')

    @vcr.use_cassette('fixtures/search-users-not-found.yml')
    def test_User_search_not_found(self):
        lms = Litmos('app-key12345', 'app-name12345')

        users = lms.User.search('beelzebub@pieshop.net')

        eq_(len(users), 0)

    @vcr.use_cassette('fixtures/find-user.yml')
    def test_User_find(self):
        lms = Litmos('app-key12345', 'app-name12345')

        user = lms.User.find('rnjx2WaQOEY1')

        eq_(user.Active, True)
        eq_(user.FirstName, 'Janine')
        eq_(user.LastName, 'Butcher')
        eq_(user.Id, 'rnjx2WaQOEY1')
        eq_(user.UserName, 'janine.butcher@pieshop.net')
        eq_(user.AccessLevel, 'Learner')
        eq_(user.Email, 'janine.butcher@pieshop.net')
