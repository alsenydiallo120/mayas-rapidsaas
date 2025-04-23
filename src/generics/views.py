from django.shortcuts import render

from generics.utils import get_project_from_app_name


def terms_of_service(request, app_name: str):
    project = get_project_from_app_name(app_name)
    context = {
        'webapp_name': project.display_name
    }
    return render(request, f'{app_name}/terms_of_service.html', context=context)


def privacy(request, app_name: str):
    project = get_project_from_app_name(app_name)
    context = {
        'webapp_name': project.display_name
    }
    return render(request, f'{app_name}/privacy.html', context=context)


def contact(request, app_name: str):
    project = get_project_from_app_name(app_name)
    context = {
        'webapp_name': project.display_name
    }
    return render(request, f'{app_name}/contact.html', context=context)
