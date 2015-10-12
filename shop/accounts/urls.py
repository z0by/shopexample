from django.conf.urls import include, url


urlpatterns = [
    url(r'^login/', 'accounts.views.login_user'),
    url(r'^logout/', 'accounts.views.logout_user'),
    url(r'^register/', 'accounts.views.register_user'),
    url(r'^confirm/(?P<activation_key>\w+)/', 'accounts.views.register_confirm'),
    url(r'^edit/','accounts.views.edit_profile'),
    url(r'^registersuccess/','accounts.views.register_success'),


]
