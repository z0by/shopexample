# -*- coding: utf-8 -*-
from os import urandom
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from .models import Cart
from .models import CartUser
from .models import Order
from .models import Good
from .forms import IndexForm
from .forms import AmmountForm
import json
from products.models import Product

def get_cart(request):
    if request.session.get('petsshopcart'):
        secret_key = request.session.get('petsshopcart')
        try:
            cart = Cart.objects.get(secret_key=secret_key)
        except Cart.DoesNotExist:
            cart = None
    else:
        cart = None
    return cart

def get_cartuser(request):
    if request.user.is_authenticated():
        try:
            cartuser = CartUser.objects.get(user=request.user)
        except CartUser.DoesNotExist:
            cartuser = CartUser(user=request.user)
            cartuser.save()
    else:
        return None
    return cartuser

def remove(request, order_id, good_id):
    cart = get_cart(request)
    cartuser = get_cartuser(request)
    try:
        order = Order.objects.get(id=order_id, cartuser=cartuser)
    except Order.DoesNotExist:
        try:
            order = Order.objects.get(id=order_id, cart=cart)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
    good = get_object_or_404(Good, order=order, id=good_id)
    good.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add(request, product_id):
    cart = get_cart(request)
    if not cart:
        secret_key = urandom(12).encode('hex')
        cart = Cart(secret_key=secret_key)
        request.session['petsshopcart'] = secret_key
        cart.save()
    good_type = get_object_or_404(Product, id=product_id)
    try:
        order = Order.objects.get(cart=cart, status=u'не отправлен')
    except Order.DoesNotExist:
        order = Order()
        order.cart = cart
        order.save()
    try:
        good = order.good_set.get(good_type = good_type)
        if good:
            good.ammount += 1
            good.save()
    except Good.DoesNotExist:
        good = Good()
        good.good_type = good_type
        good.order = order
        good.save()
    if request.is_ajax():
        items_in_cart = order.get_count

        return HttpResponse(json.dumps({'items_in_cart': items_in_cart}), content_type="application/json")
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    request.session['petsshopcart'] = cart.secret_key
    return response

def index(request):
    cart = get_cart(request)
    cartuser = get_cartuser(request)
    try:
        order = Order.objects.get(cart=cart, status=u'не отправлен')
    except Order.DoesNotExist:
        order = None
    if order:
        if request.method == 'POST':
            indexform = IndexForm(request.POST)
            if indexform.is_valid():
                order.self_delivery = indexform.cleaned_data['self_delivery']
                order.delivery_adress = indexform.cleaned_data['delivery_adress']
                order.delivery_time = indexform.cleaned_data['delivery_time']
                order.contact_phone = indexform.cleaned_data['contact_phone']
                for good in order.good_set.all():
                    if good.good_type.sale_price:
                        good.fixed_price = good.good_type.sale_price
                    else:
                        good.fixed_price = good.good_type.price
                    good.save()
                order.timestamp = timezone.now()
                order.status = u'ожидание'
                if cartuser:
                    order.cartuser = cartuser
                order.save()
                response = render(request, 'cookiecart/thanks.html')
                response.delete_cookie('petsshopcart')
                return response
        else:
            indexform = IndexForm()
    else:
        return render(request, 'cookiecart/index.html', {'cart': cart})
    return render(request, 'cookiecart/index.html', {'order': order, 'indexform': indexform, 'cart': cart})

def edit(request, order_id):
    cartuser = get_cartuser(request)
    order = get_object_or_404(Order, cartuser=cartuser, id=order_id)
    if order.status not in (u'ожидание', u'отменен пользователем'):
        return render(request, 'cookiecart/err.html', {'err': u'Нельзя изменить заказ. Свяжитесь с менеджером'})
    if request.method == 'POST':
        editform = IndexForm(request.POST)
        if editform.is_valid():
            order.self_delivery = editform.cleaned_data['self_delivery']
            order.delivery_adress = editform.cleaned_data['delivery_adress']
            order.delivery_time = editform.cleaned_data['delivery_time']
            order.contact_phone = editform.cleaned_data['contact_phone']
            order.save()
            return HttpResponseRedirect('/cart/history')
    else:
        editform = IndexForm(initial={'self_delivery': order.self_delivery, \
                                    'delivery_adress': order.delivery_adress, \
                                    'delivery_time': order.delivery_time, \
                                    'contact_phone': order.contact_phone})
    return render(request, 'cookiecart/edit.html', {'order': order, 'editform': editform})

def changeammount(request, order_id, good_id):
    cart = get_cart(request)
    try:
        order = Order.objects.get(cart=cart, id=order_id)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")
    good = get_object_or_404(Good, order=order, id=good_id)
    if request.method == 'POST':
        ammountform = AmmountForm(request.POST)
        if ammountform.is_valid():
            good.ammount = ammountform.cleaned_data['ammount']
            good.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def history(request):
    cartuser = get_cartuser(request)
    if not cartuser:
        return render(request, 'cookiecart/err.html', {'err': u'Незарегистрированные пользователи не могут просматривать историю заказов'})
    context = {'orders': cartuser.order_set.all()}
    return render(request, 'cookiecart/history.html', context)
    
def status(request, order_id, status_id):
    cartuser = get_cartuser(request)
    order = get_object_or_404(Order, cartuser=cartuser, id=order_id)
    if order.status == u'ожидание' and status_id == '4':
        order.status = u'отменен пользователем'
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
