import json

import requests


class API(object):
    ROOT_URL = 'https://api.litmos.com/v1.svc/'
    PAGINATION_OFFSET = 200
    api_key = None
    app_name = None

    @classmethod
    def _base_url(cls, resource, **kwargs):
        return cls.ROOT_URL + \
            resource + \
            ("/" + kwargs['resource_id'] if kwargs.get('resource_id', None) else "") + \
            ("/" + kwargs['sub_resource'] if kwargs.get('sub_resource', None) else "") + \
            ("/" + kwargs['sub_resource_id'] if kwargs.get('sub_resource_id', None) else "") + \
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
    def delete(cls, resource, resource_id):
        response = requests.delete(
            cls._base_url(resource,
                          resource_id=resource_id
                          )
        )

        return response.status_code == 200

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
    def update(cls, resource, resource_id, attributes):
        response = requests.put(
            cls._base_url(resource, resource_id=resource_id),
            json=attributes
        )

        if response.status_code == 404:
            return None

        if response.text:
            return json.loads(response.text)
        else:
            return {}


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

    @classmethod
    def get_children(cls, resource, resource_id):
        response = requests.get(
            cls._base_url(resource, resource_id=resource_id, sub_resource=resource)
        )

        if response.status_code == 404:
            return None

        return json.loads(response.text)

    @classmethod
    def get_sub_resource(cls, resource, resource_id, sub_resource):
        response = requests.get(
            cls._base_url(
                resource,
                resource_id=resource_id,
                sub_resource=sub_resource
            )
        )

        if response.status_code == 404:
            return None

        return json.loads(response.text)

    @classmethod
    def add_sub_resource(cls, resource, resource_id, sub_resource, attributes):
        response = requests.post(
            cls._base_url(
                resource,
                resource_id=resource_id,
                sub_resource=sub_resource
            ),
            json=attributes
        )

        if response.status_code is not 201:
            return False
        elif not response.text:
            return True
        else:
            return json.loads(response.text)

    @classmethod
    def update_sub_resource(cls, resource, resource_id, sub_resource, sub_resource_id):
        response = requests.put(
            cls._base_url(
                resource,
                resource_id=resource_id,
                sub_resource=sub_resource,
                sub_resource_id=sub_resource_id
            ),
        )

        if response.status_code is not 201:
            return False
        elif not response.text:
            return True
        else:
            return json.loads(response.text)


    @classmethod
    def remove_sub_resource(cls, resource, resource_id, sub_resource, sub_resource_id):
        response = requests.delete(
            cls._base_url(resource,
                          resource_id=resource_id,
                          sub_resource=sub_resource,
                          sub_resource_id=sub_resource_id)
        )

        return response.status_code == 200

