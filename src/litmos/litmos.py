import inflect
import json
import requests

p = inflect.engine()


class Payload(object):
    def __init__(self, j):
        self.__dict__ = j


class Litmos(object):
    ACCEPTABLE_TYPES = ['User', 'Team']

    def __init__(self, api_key, app_name):
        self.litmos_api = LitmosAPI(api_key, app_name)

    def __getattr__(self, name):
        if name in Litmos.ACCEPTABLE_TYPES:
            return LitmosType(name, self.litmos_api)
        else:
            return object.__getattribute__(self, name)


class LitmosAPI(object):
    ROOT_URL = 'https://api.litmos.com/v1.svc/'
    PAGINATION_OFFSET = 200

    def __init__(self, api_key, app_name):
        self.api_key = api_key
        self.app_name = app_name

    def _base_url(self, resource, **kwargs):
        return self.ROOT_URL + \
            resource + \
            ("/" + kwargs['resource_id'] if kwargs.get('resource_id', None) else "") + \
            '?apikey=' + self.api_key + \
            '&source=' + self.app_name + \
            '&format=json' + \
            ("&search=" + str(kwargs['search_param']) if kwargs.get('search_param', None) else "") + \
            ("&limit=" + str(kwargs['limit']) if kwargs.get('limit', None) else "") + \
            ("&start=" + str(kwargs['start']) if kwargs.get('start', None) else "")

    def find(self, resource, resource_id):
        response = requests.get(
            self._base_url(resource, resource_id=resource_id)
        )

        if response.status_code == 404:
            return None

        return json.loads(response.text)

    def _get_all(self, resource, results, start_pos):
        response = requests.get(
            self._base_url(resource, limit=self.PAGINATION_OFFSET, start=start_pos)
        )

        response_list = json.loads(response.text)

        results += response_list

        if not response_list:
            return results
        else:
            return self._get_all(resource, results, start_pos + self.PAGINATION_OFFSET)

    def all(self, resource):
        return self._get_all(resource, [], 0)

    def search(self, resource, search_param):
        response = requests.get(
            self._base_url(resource, search_param=search_param)
        )

        if response.status_code == 404:
            return None

        return json.loads(response.text)


class LitmosType(object):
    def __init__(self, object_name, litmos_api):
        self.resource_name = p.plural(object_name.lower())
        self.litmos_api = litmos_api

    def find(self, id):
        return self._parse_response(
            self.litmos_api.find(self.resource_name, id)
        )

    def all(self):
        return self._parse_response(
            self.litmos_api.all(self.resource_name)
        )

    def search(self, search_param):
        return self._parse_response(
            self.litmos_api.search(self.resource_name, search_param)
        )

    @staticmethod
    def _parse_response(response):
        if type(response) is list:
            return [Payload(elem) for elem in response]
        else:
            return Payload(response)
