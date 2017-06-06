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

        return API.update_sub_resource(
            'results',
            None,
            'modules',
            module_id,
            attributes
        )
