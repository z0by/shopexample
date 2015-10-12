# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import ManagerUser
from cookiecart.models import Order

def get_manageruser(request):
    if request.user.is_authenticated():
        try:
            manageruser = ManagerUser.objects.get(user=request.user)
        except ManagerUser.DoesNotExist:
            manageruser = ManagerUser(user=request.user)
            manageruser.save()
    else:
        raise PermissionDenied
    return manageruser

def index(request):
    manageruser = get_manageruser(request)
    return render(request, 'management/index.html', {'orders': manageruser.order_set.all()})

def waiting(request):
    manageruser = get_manageruser(request)
    return render(request, 'management/waiting.html', {'orders': Order.objects.filter(status=u'ожидание')})

def detail(request, order_id):
    manageruser = get_manageruser(request)
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'management/detail.html', {'order': order})

def status(request, order_id, status_id):
    manageruser = get_manageruser(request)
    order = get_object_or_404(Order, id=order_id)
    if order.status == u'ожидание' and status_id == '2':
        order.status = u'обработка'
        order.manageruser = manageruser
        order.save()
    if order.status == u'обработка':
        if status_id == '1':
            order.status = u'ожидание'
            order.manageruser = None
            order.save()
        elif status_id == '3':
            order.status = u'отменен менеджером'
            order.save()
        elif status_id == '5':
            order.status = u'завершен'
            order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
