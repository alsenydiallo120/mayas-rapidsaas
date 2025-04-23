from django.urls import path

from . import views

urlpatterns = [
    path('product_page/<str:product_name>', views.product_page, name='product_page'),
    path('payment_processing', views.payment_processing, name='payment_processing'),
    path('payment_status_verif', views.payment_status_verif, name='payment_status_verif'),
    path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
    path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
]
