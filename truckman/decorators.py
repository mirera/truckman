from functools import wraps
from django.shortcuts import render

def has_permission(user, required_permission):
    # Check if the user has the required permission
    if user.is_authenticated and user.is_active:
        return user.has_perm(required_permission)
    return False

def permission_required(required_permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if has_permission(request.user, required_permission):
                # User has the permission, allow access to the view
                return view_func(request, *args, **kwargs)
            else:
                # User does not have the permission, restrict access and show appropriate message via HttpResponse
                return render(request, 'error/access-denied.html')        
        return _wrapped_view
    return decorator

