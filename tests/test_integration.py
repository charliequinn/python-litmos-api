import vcr
from nose.tools import eq_, assert_true, assert_false

from litmos.litmos import Litmos


class TestLitmosIntegration():
    def setUp(self):
        self.lms = Litmos('app-key12345', 'app-name12345')

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
