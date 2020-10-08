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
        ('DisableMessages', False),
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
        ('ManagerId', ''),
    ])

    def deactivate(self):
        self.Active = False
        return self.save()

    def teams(self):
        from litmos.team import Team
        return Team._parse_response(
            API.get_sub_resource(
                self.__class__.name(),
                self.Id,
                'teams'
            )
        )

    def courses(self):
        from litmos.course import Course
        return Course._parse_response(
            API.get_sub_resource(
                self.__class__.name(),
                self.Id,
                'courses'
            )
        )
    
    def set_manager(self, manager):
        if type(manager)==User:
            self.ManagerId = manager.Id
        else:
            self.ManagerId = manager
        return self.save()

    def remove_teams(self):
        return API.remove_sub_resource(
            self.__class__.name(),
            self.Id,
            'teams',
            None
        )

    def update_advanced_custom_fields(self, data: list):
        """Takes a list of dictionaries in the format {'<FIELDNAME>':'<VALUE>'}.
        Advanced custom userfields may not be enabled by default"""
        return API.add_sub_resource(
            self.__class__.name(),
            self.Id,
            'usercustomfields',
            data
        )

    @classmethod
    def all(cls, full_details=False):
        users = super().all()

        if not full_details:
            return users

        return [cls.find(user.Id) for user in users]
