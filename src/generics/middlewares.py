from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import redirect, render

from generics.models import Project
from generics.utils import get_domain


class DynamicDomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain = get_domain(request)
        project: Project = settings.MULTI_SITE_PATTERNS.get(domain)

        # Ce "if" est à retirer une fois que tout est bien setup :)
        if project is None:
            if sorted(list(settings.MULTI_SITE_PATTERNS.keys())) == sorted(['localhost', '127.0.0.1']):
                if request.path == '/healthcheck':
                    return HttpResponse('ok')
                return render(request, "generics/welcome.html")
            return HttpResponseNotFound("<h1>Page not found</h1>")

        if request.path == '/':
            return redirect(f"{project.app_name}/")

        if (not request.path.startswith(f'/{project.app_name}')
                and request.path[1:].split('/')[0] in [p.app_name for p in settings.MULTI_SITE_PATTERNS.values()]):
            return HttpResponseNotFound("<h1>Page not found</h1>")

        response = self.get_response(request)
        return response
