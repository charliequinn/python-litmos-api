import datetime
from collections import OrderedDict

from litmos.litmos import LitmosType
from litmos.api import API
from litmos.course_module import CourseModule


class Course(LitmosType):
    SCHEMA = OrderedDict([
        ('Id', ''),
        ('Name', ''),
        ('Description', ''),
        ('Code', ''),
        ('Active', ''),
        ('ForSale', ''),
        ('OriginalId', ''),
        ('EcommerceShortDescription', ''),
        ('EcommerceLongDescription', ''),
        ('CourseCodeForBulkImport', ''),
        ('Price', ''),
        ('AccessTillDate', ''),
        ('AccessTillDays', '')
    ])

    def modules(self):
        return CourseModule._parse_response(
            API.get_sub_resource(
                self.__class__.name(),
                self.Id,
                'modules'
            )
        )

    def module_complete(self, module_id, attributes):
        attributes['CourseId'] = self.Id

        iso_8601_date = attributes['UpdatedAt']

        updated_at_datetime = datetime.datetime.strptime(iso_8601_date, '%Y-%m-%dT%H:%M:%S.%fZ')

        epoch_datetime = int(updated_at_datetime.timestamp() * 1000)

        attributes['UpdatedAt'] = "/Date({0})/".format(epoch_datetime)

        return API.update_sub_resource(
            'results',
            None,
            'modules',
            module_id,
            attributes
        )
