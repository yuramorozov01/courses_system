from base_app.permissions import CustomBasePermission
from rest_framework import permissions


class IsCourseAuthor(CustomBasePermission):
    '''Object-level permission to only allow author of a course to manipulate with data.
    Assumes the user model instance has an `own_courses` attribute.
    '''

    message = 'Only author is allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'own_courses', 'course_pk')


class IsCourseTeacher(CustomBasePermission):
    '''Object-level permission to only allow teachers of a course to manipulate with data.
    Assumes the user model instance has an `teaching_courses` attribute.
    '''

    message = 'Only teachers are allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'teaching_courses', 'course_pk')


class IsCourseStudent(CustomBasePermission):
    '''Object-level permission to only allow students of a course to manipulate with data.
    Assumes the user model instance has an `attending_courses` attribute.
    '''

    message = 'Only students are allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'attending_courses', 'course_pk')


class IsCourseTeacherOrStudent(CustomBasePermission):
    '''Object-level permission to only allow teachers and students of a course to manipulate with data.
    Assumes the user model instance has an `teaching_courses` and `attending_courses` attributes.
    '''

    message = 'Only teachers and students are allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'teaching_courses', 'course_pk') or \
               self.has_permission_by_field(request, view, 'attending_courses', 'course_pk')
