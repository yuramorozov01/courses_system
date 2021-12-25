from base_app.permissions import CustomBasePermission


class IsMessageAuthor(CustomBasePermission):
    '''Object-level permission to only allow author of a message to manipulate with data.
    Assumes the user model instance has an `messages` attribute.
    '''

    message = 'Only author of task is allowed to do this.'

    def has_permission(self, request, view):
        return self.has_permission_by_field(request, view, 'messages', 'message_pk')
