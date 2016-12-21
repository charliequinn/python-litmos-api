import sys
from collections import OrderedDict
from copy import copy

import inflect

from litmos.api import API

p = inflect.engine()


class Litmos(object):
    ACCEPTABLE_TYPES = ['User', 'Team']

    def __init__(self, api_key, app_name):
        API.api_key = api_key
        API.app_name = app_name

        self.litmos_api = API

    def __getattr__(self, name):
        if name in Litmos.ACCEPTABLE_TYPES:
            return getattr(sys.modules[__name__], name)
        else:
            return object.__getattribute__(self, name)


class LitmosType(object):
    def __init__(self, attributes={}):
        self.__dict__ = dict(self.SCHEMA)

        for attr in attributes:
            setattr(self, attr, attributes[attr])

    def save(self):
        schema = copy(self.SCHEMA)
        for param in schema:
            attribute_value = getattr(self, param)
            if attribute_value is not None:
                schema[param] = attribute_value

        if self.is_new_record:
            response = API.create(self.__class__.name(), schema)
            for attr in response:
                setattr(self, attr, response[attr])
        else:
            API.update(self.__class__.name(), self.Id, schema)

        return True

    def destroy(self):
        return self.delete(self.Id)

    @property
    def is_new_record(self):
        return not self.Id

    @classmethod
    def name(cls):
        return p.plural(cls.__name__.lower())

    @classmethod
    def find(cls, id):
        return cls._parse_response(
            API.find(cls.name(), id)
        )

    @classmethod
    def all(cls):
        return cls._parse_response(
            API.all(cls.name())
        )

    @classmethod
    def search(cls, search_param):
        return cls._parse_response(
            API.search(cls.name(), search_param)
        )

    @classmethod
    def delete(cls, resource_id):
        return API.delete(cls.name(), resource_id=resource_id)

    @classmethod
    def create(cls, attributes):
        schema = copy(cls.SCHEMA)
        for param in schema:
            attribute_value = attributes.get(param, None)
            if attribute_value:
                schema[param] = attribute_value

        return cls._parse_response(
            API.create(cls.name(), schema)
        )

    @classmethod
    def _parse_response(cls, response):
        if type(response) is list:
            return [cls(elem) for elem in response]
        else:
            return cls(response)


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
        return self.__class__._parse_response(
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

        sub_team = self.__class__._parse_response(
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
            user.__class__.name(),
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
