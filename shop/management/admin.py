from django.contrib import admin

from .models import ManagerUser

class ManagerUserAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ['id', 'user']
    list_filter = ['user']
    class Meta:
        model = ManagerUser
    pass

admin.site.register(ManagerUser, ManagerUserAdmin)
