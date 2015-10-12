# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from accounts.forms import UserChangeForm, UserCreationForm

from accounts.models import AuthUser

class AuthUserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm


    list_display = ( 'username', 'email', 'phone')

class UserProfileAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm



    list_display = ( 'username', 'email', 'phone')

admin.site.register(AuthUser,  AuthUserAdmin)

