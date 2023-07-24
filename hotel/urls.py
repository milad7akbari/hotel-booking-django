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
from django.urls import path, include

from Hotel_Test import settings
from apps.front.views import home_page
from django.conf.urls.static import static

admin.site.site_header = "Hotel Tik"
admin.site.site_title = "Hotel Tik"
admin.site.index_title = "Hotel Tik"
urlpatterns = i18n_patterns(
    path('summernote/', include('django_summernote.urls')),
    path('cart/', include('apps.front.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('blog/', include('apps.blog.urls')),
    path('hotel/', include('apps.hotel.urls')),
    path('panel/', include('apps.customer.urls')),
    path('', home_page, name='home_page'),
    path("logout/", LogoutView.as_view(), name="logout"),

)

urlpatterns += [
    path('login/', include('apps.base.urls')),
    path('hotel-l/', include('apps.base.urls')),
    path('cart/', include('apps.base.urls')),

]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

