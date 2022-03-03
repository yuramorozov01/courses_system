from base_app.permissions import CustomBasePermission


class IsTaskAuthor(CustomBasePermission):
    '''Object-level permission to only allow author of a task to manipulate with data.
    Assumes the user model instance has an `own_tasks` attribute.
    '''

    message = 'Only author of task is allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'own_tasks', 'task_pk')


class IsTaskAuthorOrCourseTeacher(CustomBasePermission):
    '''Object-level permission to only allow author of a task or course teacher to manipulate with data.
    Assumes the user model instance has an `own_tasks` and `teaching_courses` attribute.
    '''

    message = 'Only author of task or course teachers are allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'own_tasks', 'task_pk') or \
               self.has_permission_by_field(request, view, 'teaching_courses', 'course_pk')
