"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.template.defaulttags import url
from django.urls import path, include, re_path
from django.views.static import serve
from django.utils.translation import gettext_lazy as _

from hotel import settings
from apps.front.views import home_page, general_policy, about_us, tracking
from django.conf.urls.static import static
handler404 = 'apps.base.views.view_404'
admin.site.site_title = _("هتل تیک")
admin.site.index_title = _("هتل تیک")
urlpatterns = i18n_patterns(
    path('summernote/', include('django_summernote.urls')),
    path('cart/', include('apps.front.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('blog/', include('apps.blog.urls')),
    path('hotel/', include('apps.hotel.urls')),
    path('panel/', include('apps.customer.urls')),
    path('general-policy', general_policy, name='generalPolicy'),
    path('tracking', tracking, name='tracking'),
    path('about-us', about_us, name='about_us'),
    path('', home_page, name='home_page'),
    path("logout/", LogoutView.as_view(), name="logout"),
)
urlpatterns += [
    path('', home_page, name='home_page'),
    path('get/', include('apps.base.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
