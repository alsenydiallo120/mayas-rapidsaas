from django.urls import path
from . import views

urlpatterns = [
    path('my_first_saas/', views.index, name='my_first_saas__index'),
    path('my_first_saas/info/tos/', views.terms_of_service, name='my_first_saas__terms_of_service'),
    path('my_first_saas/info/priv/', views.privacy, name='my_first_saas__privacy'),
    path('my_first_saas/info/contact/', views.contact, name='my_first_saas__contact'),
]
