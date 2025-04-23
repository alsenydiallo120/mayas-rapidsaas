from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('authentications.urls')),
    path('', include('payments.urls')),
    path("healthcheck/", lambda r: HttpResponse("ok"), name="healthcheck")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


for domain, pattern_name in settings.MULTI_SITE_PATTERNS.items():
    include_namespace_urls = f'{pattern_name.app_name}.urls'
    urlpatterns.append(path('', include(include_namespace_urls)))

