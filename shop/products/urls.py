from django.conf.urls import include, url


urlpatterns = [
        #url(r'^$', 'products.views.index_view',name='home'),
        url(r'^all/$', 'products.views.all', name='products'),
        url(r'^catalog/$', 'products.views.catalog', name='catalog'),
        url(r'^catalog/new_products/$', 'products.views.new_products', name='new_products'),
        url(r'^catalog/sale_products/$', 'products.views.sale_products', name='sale_products'),
        url(r'^category/(?P<category_slug>[-\w]+)/$', 'products.views.category_view', name='catalog_category'),
        url(r'^product/(?P<brand_slug>[-\w]+)/(?P<product_slug>[-\w]+)/(?P<id>\d+)/$', 'products.views.product_view',name='product_detail'),
        url(r'change_view/$', 'products.views.change_view', name='change_view'),
        url(r'sort_view/$', 'products.views.sort_view', name='sort_view'),


         #url(r'^add/$', 'products.views.product_review',name='product_review'),


]

