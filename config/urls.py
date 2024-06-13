from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

admin.site.site_header = "Energy Portfolio Contract Management"
admin.site.index_title = "Energy Portfolio Contract Management"


urlpatterns = [
    path("grappelli/", include("grappelli.urls")),  # grappelli URLS
    path("ep_crm_portal/", admin.site.urls),
    path("", include("pages.urls")),
    path("users/", include("users.urls")),
    path("clients/", include("clients.urls")),
    path("contracts/", include("contracts.urls")),
    path("select2/", include("django_select2.urls")),
    path("contacts/", include("contacts.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
