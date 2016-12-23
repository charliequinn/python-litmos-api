from collections import OrderedDict
from unittest.mock import patch

from nose.tools import assert_true

from litmos import User


class TestUser:
    @patch('litmos.litmos.API')
    def test_deactivate(self, api_mock):
        api_mock.update.return_value = True

        user = User({'Id': 'wsGth', 'Active': True})

        assert_true(user.deactivate())

        api_mock.update.assert_called_once_with(
            'users',
            'wsGth',
            OrderedDict([('Id', 'wsGth'),
                         ('UserName', ''),
                         ('FirstName', ''),
                         ('LastName', ''),
                         ('FullName', ''),
                         ('Email', ''),
                         ('AccessLevel', 'Learner'),
                         ('DisableMessages', True),
                         ('Active', False),
                         ('Skype', ''),
                         ('PhoneWork', ''),
                         ('PhoneMobile', ''),
                         ('LastLogin', ''),
                         ('LoginKey', ''),
                         ('IsCustomUsername', False),
                         ('Password', ''),
                         ('SkipFirstLogin', True),
                         ('TimeZone', 'UTC'),
                         ('Street1', ''),
                         ('Street2', ''),
                         ('City', ''),
                         ('State', ''),
                         ('PostalCode', ''),
                         ('Country', ''),
                         ('CompanyName', ''),
                         ('JobTitle', ''),
                         ('CustomField1', ''),
                         ('CustomField2', ''),
                         ('CustomField4', ''),
                         ('CustomField5', ''),
                         ('CustomField6', ''),
                         ('CustomField7', ''),
                         ('CustomField8', ''),
                         ('CustomField9', ''),
                         ('CustomField10', ''),
                         ('Culture', '')
                         ]
                        )
        )

    @patch('litmos.user.API')
    def test_remove_teams(self, api_mock):
        api_mock.remove_sub_resource.return_value = True

        user = User({'Id': 'fgUr2', 'Name': 'User1'})

        assert_true(user.remove_teams())

        api_mock.remove_sub_resource.assert_called_once_with('users',
                                                             user.Id,
                                                             'teams',
                                                             None)
