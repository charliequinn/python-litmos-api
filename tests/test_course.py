from unittest.mock import patch

from nose.tools import eq_

from litmos.course import Course


class TestCourse:
    @patch('litmos.course.API')
    def test_modules(self, api_mock):
        api_mock.get_sub_resource.return_value = [
            {'Id': 'fgUr3', 'Name': 'SubTeam1'},
            {'Id': 'fgUr2', 'Name': 'SubTeam2'}
        ]

        course = Course({'Id': 'fgUr1', 'Name': 'Team1'})

        modules = course.modules()

        eq_(2, len(modules))
        api_mock.get_sub_resource.assert_called_once_with('courses', 'fgUr1', 'modules')

    @patch('litmos.course.API')
    def test_module_complete(self, api_mock):
        api_mock.update_sub_resource.return_value = True
        course = Course({'Id': 'fgUr1', 'Name': 'Team1'})

        module_complete = course.module_complete('fg2', {'UpdatedAt': '2016-11-10T13:50:11.390Z'})

        eq_(True, module_complete)
        api_mock.update_sub_resource.assert_called_once_with(
            'results',
            None,
            'modules',
            'fg2',
            {'CourseId': course.Id, 'UpdatedAt': '/Date(1478785811390)/'}
        )
