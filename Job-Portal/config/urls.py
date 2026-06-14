
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
 
from django.contrib.sitemaps.views import sitemap
from jobapp.sitemaps import JobSitemap
from django.http import HttpResponse

sitemaps = {
    'jobs': JobSitemap,
}

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Sitemap: {}://{}/sitemap.xml".format(request.scheme, request.get_host())
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobapp.urls')),
    path('', include('account.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
