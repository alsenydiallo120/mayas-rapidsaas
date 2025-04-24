from django.shortcuts import render
from generics.views import terms_of_service as g_terms_of_service, privacy as g_privacy, contact as g_contact


def index(request):
    return render(request, 'my_first_saas/index.html')


def terms_of_service(request):
    return g_terms_of_service(request, 'my_first_saas')


def privacy(request):
    return g_privacy(request, 'my_first_saas')


def contact(request):
    return g_contact(request, 'my_first_saas')

