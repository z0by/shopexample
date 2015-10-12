# -*- coding: utf-8 -*-
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
# Register your models here.
from .models import Product, Category, ProductImage, ProductReview, Characteristic, CharacteristicType
from django.utils.translation import ugettext_lazy as _

class ProductImageAdmin(admin.StackedInline):

    model = ProductImage
    extra = 1

class CharacteristicAdmin(admin.StackedInline):
    """Добавление характеристик для продуктов"""
    model = Characteristic
    extra = 1
    fieldsets = [
        (_(u'Characteristic'), {'fields': ['characteristic_type']}),
        (_(u'Value'), {'fields': ['value']}),
    ]

class CharacteristicTypeAdmin(admin.ModelAdmin):
    """Добавление характеристик для продуктов"""
    model = CharacteristicType
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(DjangoMpttAdmin):
    """
    РЈРїСЂР°РІР»РµРЅРёРµ РєР°С‚РµРіРѕСЂРёСЏРјРё
    РљР°Рє Р±СѓРґСѓС‚ РѕС‚РѕР±СЂР°Р¶Р°С‚СЊСЃСЏ РїРѕР»СЏ РєР°С‚РµРіРѕСЂРёР№ РІ СЂР°Р·РґРµР»Рµ Р°РґРјРёРЅРёСЃС‚СЂРёСЂРѕРІР°РЅРёСЏ
    """
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    readonly_fields = ('created_at', 'updated_at',)
    # exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at' #updated
    search_fields = ['title', 'description']
    list_display = ['title', 'price','old_price', 'is_active', 'updated_at']

    list_editable = ['price','old_price','is_active']
    list_filter = ['price', 'is_active']
    readonly_fields = ['updated_at', 'created_at']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CharacteristicAdmin, ProductImageAdmin,]

    class Meta:
        model = Product

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']
    class Meta:
        model = ProductReview


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductReview, ReviewAdmin)
admin.site.register(CharacteristicType,CharacteristicTypeAdmin)
