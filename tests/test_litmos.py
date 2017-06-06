from nose.tools import raises, eq_

from litmos import Litmos
from litmos.api import API


class TestLitmos:
    def test_acceptable_types(self):
        eq_(Litmos.ACCEPTABLE_TYPES, ['User', 'Team', 'Course', 'CourseModule'])

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
