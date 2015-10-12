# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sessions.models import Session
from django.utils import timezone

from accounts.models import AuthUser
from products.models import Product
from management.models import ManagerUser

class Cart(models.Model):
    secret_key = models.CharField(max_length=48)

    def __unicode__(self):
        return u'{} cookie cart'.format(self.secret_key)

class CartUser(models.Model):
    user = models.ForeignKey(AuthUser)

    def __unicode__(self):
        return u'{} cartuser'.format(self.user)

class Order(models.Model):
    STATUS_CHOICES = (
        (u'не отправлен', u'не отправлен'),
        (u'ожидание', u'ожидание'),
        (u'обработка', u'обработка'),
        (u'отменен менеджером', u'отменен менеджером'),
        (u'отменен пользователем', u'отменен пользователем'),
        (u'завершен', u'завершен'))
    cart = models.ForeignKey(Cart, null=True)
    cartuser = models.ForeignKey(CartUser, null=True)
    manageruser = models.ForeignKey(ManagerUser, null=True)
    timestamp = models.DateTimeField(default=timezone.now())
    status = models.CharField(max_length=20, choices = STATUS_CHOICES, default=u'не отправлен')
    self_delivery = models.BooleanField(default=False)
    delivery_adress = models.CharField(max_length=100, null=True)
    delivery_time = models.CharField(max_length=50, null=True)
    contact_phone = models.CharField(max_length=15, null=True)

    def __unicode__(self):
        return u'Order in {}'.format(self.cart)

    def get_total(self):
        total = 0
        for good in self.good_set.all():
            if good.fixed_price:
                total += good.fixed_price*good.ammount
            # elif good.good_type.price < good.good_type.old_price:
            #     total += good.good_type.sale_price*good.ammount
            else:
                total += good.good_type.price*good.ammount
        return total

    @property
    def get_count(self):
        total = 0
        for good in self.good_set.all():
            total += good.ammount
        return total

class Good(models.Model):
    good_type = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    ammount = models.IntegerField(default=1)
    fixed_price = models.DecimalField(decimal_places=2, max_digits=100, null=True)
