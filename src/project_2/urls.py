from django.urls import path
from . import views

urlpatterns = [
    path('project_2/', views.index, name='project_2__index'),
    path('project_2/info/tos/', views.terms_of_service, name='project_2__terms_of_service'),
    path('project_2/info/priv/', views.privacy, name='project_2__privacy'),
    path('project_2/info/contact/', views.contact, name='project_2__contact'),
]
