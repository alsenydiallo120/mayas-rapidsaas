from django.contrib.auth import logout
from django.shortcuts import redirect

from generics.utils import get_site_name


def logout_view(request):
    logout(request)
    return redirect(f'{get_site_name(request)}__index')
