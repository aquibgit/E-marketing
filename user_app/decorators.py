from django.shortcuts import redirect
from emarketing.views import login

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("uid"):
            return redirect(login)
        return view_func(request, *args, **kwargs)
    return wrapper