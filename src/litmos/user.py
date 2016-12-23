from collections import OrderedDict

from litmos.api import API
from litmos.litmos import LitmosType


class User(LitmosType):
    SCHEMA = OrderedDict([
        ('Id', ''),
        ('UserName', ''),
        ('FirstName', ''),
        ('LastName', ''),
        ('FullName', ''),
        ('Email', ''),
        ('AccessLevel', 'Learner'),
        ('DisableMessages', True),
        ('Active', True),
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
        ('Culture', ''),
    ])

    def deactivate(self):
        self.Active = False
        return self.save()

    def remove_teams(self):
        return API.remove_sub_resource(
            self.__class__.name(),
            self.Id,
            'teams',
            None
        )
