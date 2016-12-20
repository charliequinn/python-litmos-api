import inflect
import json
import requests
import sys

from collections import OrderedDict
from copy import copy

p = inflect.engine()


class Litmos(object):
    ACCEPTABLE_TYPES = ['User', 'Team']

    def __init__(self, api_key, app_name):
        LitmosAPI.api_key = api_key
        LitmosAPI.app_name = app_name

        self.litmos_api = LitmosAPI

    def __getattr__(self, name):
        if name in Litmos.ACCEPTABLE_TYPES:
            return getattr(sys.modules[__name__], name)
        else:
            return object.__getattribute__(self, name)


class LitmosAPI(object):
    ROOT_URL = 'https://api.litmos.com/v1.svc/'
    PAGINATION_OFFSET = 200
    api_key = None
    app_name = None

    @classmethod
    def _base_url(cls, resource, **kwargs):
        return cls.ROOT_URL + \
            resource + \
            ("/" + kwargs['resource_id'] if kwargs.get('resource_id', None) else "") + \
            '?apikey=' + cls.api_key + \
            '&source=' + cls.app_name + \
            '&format=json' + \
            ("&search=" + str(kwargs['search_param']) if kwargs.get('search_param', None) else "") + \
            ("&limit=" + str(kwargs['limit']) if kwargs.get('limit', None) else "") + \
            ("&start=" + str(kwargs['start']) if kwargs.get('start', None) else "")

    @classmethod
    def find(cls, resource, resource_id):
        response = requests.get(
            cls._base_url(resource, resource_id=resource_id)
        )

        if response.status_code == 404:
            return None

        return json.loads(response.text)

    @classmethod
    def create(cls, resource, attributes):
        response = requests.post(
            cls._base_url(resource),
            json=attributes
        )

        if response.status_code == 404:
            return None

        return json.loads(response.text)

    @classmethod
    def search(cls, resource, search_param):
        response = requests.get(
            cls._base_url(resource, search_param=search_param)
        )

        if response.status_code == 404:
            return None

        return json.loads(response.text)

    @classmethod
    def _get_all(cls, resource, results, start_pos):
        response = requests.get(
            cls._base_url(resource, limit=cls.PAGINATION_OFFSET, start=start_pos)
        )

        response_list = json.loads(response.text)
        results += response_list

        if not response_list:
            return results
        else:
            return cls._get_all(resource, results, start_pos + cls.PAGINATION_OFFSET)

    @classmethod
    def all(cls, resource):
        return cls._get_all(resource, [], 0)


class LitmosType(object):
    def __init__(self, j):
        self.__dict__ = j

    @classmethod
    def name(cls):
        return p.plural(cls.__name__.lower())

    @classmethod
    def find(cls, id):
        return cls._parse_response(
            LitmosAPI.find(cls.name(), id)
        )

    @classmethod
    def all(cls):
        return cls._parse_response(
            LitmosAPI.all(cls.name())
        )

    @classmethod
    def search(cls, search_param):
        return cls._parse_response(
            LitmosAPI.search(cls.name(), search_param)
        )

    @classmethod
    def create(cls, attributes):
        schema = copy(cls.SCHEMA)
        for param in schema:
            attribute_value = attributes.get(param, None)
            if attribute_value:
                schema[param] = attribute_value

        return cls._parse_response(
            LitmosAPI.create(cls.name(), schema)
        )

    @classmethod
    def _parse_response(cls, response):
        if type(response) is list:
            return [cls(elem) for elem in response]
        else:
            return cls(response)


class Team(LitmosType):
    pass


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
