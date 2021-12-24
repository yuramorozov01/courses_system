from rest_framework import permissions


class CoursePermission(permissions.BasePermission):
    '''Course base permission with retrieving entry of course in specified field.'''

    def get_course_pk(self, view):
        course_pk = view.kwargs.get('course_pk')
        if course_pk is None:
            course_pk = view.kwargs.get('pk')
        return course_pk

    def has_permission_by_field(self, request, view, field):
        course_pk = self.get_course_pk(view)
        if course_pk is not None:
            try:
                data_field = getattr(request.user, field)
                data = data_field.all().filter(pk=course_pk)
                if data.exists():
                    return True
            except AttributeError:
                return False
        return False


class IsCourseAuthor(CoursePermission):
    '''Object-level permission to only allow author of a course to manipulate with data.
    Assumes the user model instance has an `own_courses` attribute.
    '''

    message = 'Only author is allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'own_courses')


class IsCourseTeacher(CoursePermission):
    '''Object-level permission to only allow teachers of a course to manipulate with data.
    Assumes the user model instance has an `teaching_courses` attribute.
    '''

    message = 'Only teachers are allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'teaching_courses')


class IsCourseStudent(CoursePermission):
    '''Object-level permission to only allow students of a course to manipulate with data.
    Assumes the user model instance has an `attending_courses` attribute.
    '''

    message = 'Only students are allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'attending_courses')


class IsCourseTeacherOrStudent(CoursePermission):
    '''Object-level permission to only allow teachers and students of a course to manipulate with data.
    Assumes the user model instance has an `teaching_courses` and `attending_courses` attributes.
    '''

    message = 'Only teachers and students are allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'teaching_courses') or \
               self.has_permission_by_field(request, view, 'attending_courses')
