import os

from django.conf import settings

from generics.models import Project


def get_project_from_app_name(site_name: str) -> Project:
    for domain, project in settings.MULTI_SITE_PATTERNS.items():
        if project.app_name == site_name:
            return project
    raise Exception(f"No matching project found for site {site_name}")


def get_domain(request) -> str:
    host = request.get_host()
    domain = host.split(':')[0]
    return domain


def get_site_name(request) -> str:
    current_domain = get_domain(request)
    for mapped_domain, project in settings.MULTI_SITE_PATTERNS.items():
        if current_domain == mapped_domain:
            return project.app_name
    raise Exception(f"No matching project found for site {current_domain}")


def create_dir_if_not_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
