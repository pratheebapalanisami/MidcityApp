from django.core.exceptions import PermissionDenied


def user_is_organization(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'organization':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_volunteer(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'volunteer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
