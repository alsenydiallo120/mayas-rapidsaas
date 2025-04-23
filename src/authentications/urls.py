from django.urls import path, include

from authentications import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('', include('allauth.socialaccount.urls')),
    path('logout', views.logout_view, name='authentications__logout'),
]
