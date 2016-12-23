from copy import copy

import inflect

from litmos.api import API

p = inflect.engine()


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
    def find(cls, resource_id):
        return cls._parse_response(
            API.find(cls.name(), resource_id)
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
