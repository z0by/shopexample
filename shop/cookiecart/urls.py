from django.conf.urls import include, url


urlpatterns = [
        url(r'^add/(?P<product_id>[0-9]+)/$', 'cookiecart.views.add', name='add'),
        url(r'^remove/(?P<order_id>[0-9]+)/(?P<good_id>[0-9]+)/$', 'cookiecart.views.remove', name='remove'),
        url(r'^edit/(?P<order_id>[0-9]+)/$', 'cookiecart.views.edit', name='edit'),
        url(r'^status/(?P<order_id>[0-9]+)/(?P<status_id>[0-5]+)/$', 'cookiecart.views.status', name='status'),
        url(r'^changeammount/(?P<order_id>[0-9]+)/(?P<good_id>[0-9]+)/$', 'cookiecart.views.changeammount', name='changeammount'),
        url(r'^$', 'cookiecart.views.index', name='index'),
        url(r'^history/$', 'cookiecart.views.history', name='history'),
]
