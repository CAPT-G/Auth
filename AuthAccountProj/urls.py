from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import page_not_found, server_error

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls", namespace="accounts")),
]

# Custom error handlers (templates in /templates/404.html, /templates/500.html)
handler404 = "AccountAuthProj.urls.custom_404"
handler500 = "AccountAuthProj.urls.custom_500"

def custom_404(request, exception):
    return page_not_found(request, exception, template_name="404.html")

def custom_500(request):
    return server_error(request, template_name="500.html")

# In DEBUG, serve static/media via Django (WhiteNoise handles static even in prod)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
