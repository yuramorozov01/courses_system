from rest_framework import permissions


class CustomBasePermission(permissions.BasePermission):
    '''Custom base permission with retrieving entry of object with primary key in kwargs in specified field.'''

    def get_kwarg_pk(self, view, kwarg):
        pk = view.kwargs.get(kwarg)
        if pk is None:
            pk = view.kwargs.get('pk')
        return pk

    def has_permission_by_field(self, request, view, field, kwarg):
        pk = self.get_kwarg_pk(view, kwarg)
        if pk is not None:
            try:
                data_field = getattr(request.user, field)
                data = data_field.all().filter(pk=pk)
                if data.exists():
                    return True
            except AttributeError:
                return False
        return False
