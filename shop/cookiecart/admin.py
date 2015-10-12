from django.contrib import admin

from .models import Cart, CartUser, Order, Good

class CartAdmin(admin.ModelAdmin):
    search_fields = ['secret_key']
    list_display = ['id', 'secret_key']
    list_filter = ['secret_key']
    class Meta:
        model = Cart
    pass

class CartUserAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ['id', 'user']
    list_filter = ['user']
    class Meta:
        model = CartUser
    pass

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['cart']
    list_display = ['id', 'cart', 'timestamp', 'status', \
                    'delivery_adress', 'delivery_time', 'contact_phone']
    list_filter = ['cart']
    class Meta:
        model = Order
    pass

class GoodAdmin(admin.ModelAdmin):
    search_fields = ['good_type']
    list_display = ['id', 'good_type', 'ammount', 'fixed_price']
    list_filter = ['good_type']
    class Meta:
        model = Good
    pass

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(CartUser, CartUserAdmin)
