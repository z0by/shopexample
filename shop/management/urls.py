from django.conf.urls import include, url


urlpatterns = [
        url(r'^$', 'management.views.index', name='index'),
        url(r'^waiting/$', 'management.views.waiting', name='waiting'),
        url(r'^detail/(?P<order_id>[0-9]+)/$', 'management.views.detail', name='detail'),
        url(r'^status/(?P<order_id>[0-9]+)/(?P<status_id>[0-5]+)/$', 'management.views.status'),
]
