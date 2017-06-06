from collections import OrderedDict

from litmos.litmos import LitmosType


class CourseModule(LitmosType):
    SCHEMA = OrderedDict([
        ('Id', ''),
        ('Name', ''),
        ('Description', ''),
        ('Code', '')
    ])

