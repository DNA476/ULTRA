from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from .permissions import user_has_any_role


def role_required(*roles, raise_exception=True):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if user_has_any_role(request.user, roles):
                return view_func(request, *args, **kwargs)
            if raise_exception:
                raise PermissionDenied
            return redirect_to_login(request.get_full_path())
        return wrapper
    return decorator
