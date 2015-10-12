# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from .models import Order

class IndexForm(forms.Form):
    self_delivery = forms.BooleanField(label=u'Самовывоз', required=False, widget=forms.CheckboxInput(attrs={'onchange': "changeActive()"}))
    delivery_adress = forms.CharField(label=u'Адрес доставки', max_length=100, required=False, widget=forms.TextInput(attrs={'size': '60'}))
    delivery_time = forms.CharField(label=u'Время доставки', max_length=50, required=False, widget=forms.TextInput(attrs={'size': '60'}))
    contact_phone = forms.CharField(label=u'Контактный телефон', max_length=15, widget=forms.TextInput(attrs={'size': '20'}))

    def clean(self):
        cleaned_data = super(IndexForm, self).clean()
        if not cleaned_data['self_delivery'] and not (cleaned_data['delivery_adress'] and cleaned_data['delivery_time']):
            raise ValidationError((u"Введите адрес доставки и удобное время доставки или выберите самовывоз"), code='invalid')
        return cleaned_data

class AmmountForm(forms.Form):
    ammount = forms.IntegerField()

    def clean(self):
        cleaned_data = super(AmmountForm, self).clean()
        if cleaned_data and cleaned_data['ammount'] <= 0:
            raise ValidationError((u"Недопустимое количество"), code='illegal')
        return cleaned_data
