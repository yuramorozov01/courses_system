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
