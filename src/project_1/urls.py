from django.urls import path
from . import views

urlpatterns = [
    path('project_1/', views.index, name='project_1__index'),
    path('project_1/info/tos/', views.terms_of_service, name='project_1__terms_of_service'),
    path('project_1/info/priv/', views.privacy, name='project_1__privacy'),
    path('project_1/info/contact/', views.contact, name='project_1__contact'),
]
