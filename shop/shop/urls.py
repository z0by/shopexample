"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from accounts import urls as accounts_urls
from products import urls as products_urls
#from cart import urls as cart_urls
from django.conf.urls import include, patterns, url
from cookiecart import urls as cart_urls
from management import urls as management_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','products.views.index_view',name='home'),
    url(r'', include('social_auth.urls')),
    url(r'', include('password_reset.urls')),
    url(r'^account/', include(accounts_urls)),
    url(r'^products/', include(products_urls)),
    url(r'^cart/', include(cart_urls)),
    url(r'^management/', include(management_urls)),
    url(r'^review/add/$', 'products.views.product_review',name='product_review'),
    url(r'^search/$', 'products.views.search',name='search'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )