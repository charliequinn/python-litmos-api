import sys

from litmos.api import API
from litmos.litmos import LitmosType
from litmos.team import Team
from litmos.user import User

__version__ = "0.1.2"


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
