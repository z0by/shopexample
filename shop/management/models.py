# -*- coding: utf-8 -*-
from django.db import models

from accounts.models import AuthUser

class ManagerUser(models.Model):
    user = models.OneToOneField(AuthUser)

    def clean(self):
        if self.user.is_staff == False:
            raise ValidationError(u'Ошибка доступа')
