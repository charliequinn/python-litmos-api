from collections import OrderedDict
from copy import copy

from litmos.litmos import LitmosType
from litmos.api import API
from litmos.user import User


class Team(LitmosType):
    SCHEMA = OrderedDict([
        ('Id', ''),
        ('Name', ''),
        ('Description', '')
    ])

    USER_SCHEMA = OrderedDict([
        ('Id', ''),
        ('UserName', ''),
        ('FirstName', ''),
        ('LastName', '')
    ])

    def sub_teams(self):
        return self._parse_response(
            API.get_sub_resource(
                self.__class__.name(),
                self.Id,
                self.__class__.name()
            )
        )

    def users(self):
        return User._parse_response(
            API.get_sub_resource(
                self.__class__.name(),
                self.Id,
                'users'
            )
        )

    def leaders(self):
        return User._parse_response(
            API.get_sub_resource(
                self.__class__.name(),
                self.Id,
                'leaders'
            )
        )

    def add_sub_team(self, sub_team):
        schema = copy(self.SCHEMA)
        for param in schema:
            attribute_value = getattr(sub_team, param)
            if attribute_value is not None:
                schema[param] = attribute_value

        sub_team = self._parse_response(
            API.add_sub_resource(
                self.__class__.name(),
                self.Id,
                self.__class__.name(),
                schema
            )
        )

        return sub_team.Id

    def add_users(self, users):
        user_list = []
        for user in users:
            schema = copy(self.USER_SCHEMA)
            for param in schema:
                attribute_value = getattr(user, param)
                if attribute_value is not None:
                    schema[param] = attribute_value

            user_list.append(schema)

        return API.add_sub_resource(
            self.__class__.name(),
            self.Id,
            User.name(),
            user_list
        )

    def remove_user(self, user):
        return API.remove_sub_resource(
            self.__class__.name(),
            self.Id,
            'users',
            user.Id
        )

    def promote_team_leader(self, user):
        return API.update_sub_resource(
            self.__class__.name(),
            self.Id,
            'leaders',
            user.Id
        )

    def demote_team_leader(self, user):
        return API.remove_sub_resource(
            self.__class__.name(),
            self.Id,
            'leaders',
            user.Id
        )
