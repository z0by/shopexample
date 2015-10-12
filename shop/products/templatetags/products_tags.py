from django import template
from products.models import Category
from cookiecart.models import Order,Cart
from cookiecart.views import get_cart
import re


register = template.Library()


@register.inclusion_tag("tags/category_listnew1.html")
def categories_tree(request):
    return {'nodes': Category.objects.filter(is_active=True) }

@register.simple_tag()
def cart_box(request):
    try:
        cart = get_cart(request)
    except Cart.DoesNotExist:
        cart = None
    try:
        order = Order.objects.get(cart=cart)

    except Order.DoesNotExist:
        order = None

    if order:
        return '<span id="items_in_cart">{}</span>'.format(order.get_count)
    else:
        return  '<span id="items_in_cart"></span>'


@register.simple_tag
def active(request, pattern):
    try:
        if re.search(pattern, request.path):
            return 'class="active"'
        return ''
    except Exception:
        return ''