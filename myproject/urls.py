import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from accounts.views import LoginView

from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', LoginView.as_view(), name='login'),
    path('accounts/', include('accounts.urls',namespace='accounts')),
    path('branch/', include('branch.urls',namespace='branch')),
    path('lead/', include('lead_management.urls',namespace='lead_management')),



    path('jsi18n', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]


if settings.FORCE_STATIC_FILE_SERVING and not settings.DEBUG:
    settings.DEBUG = True
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    settings.DEBUG = False


admin.site.site_header = "CRM Admin"
admin.site.site_title = "CRM Admin Portal"
admin.site.index_title = "CRM Researcher Portal"
