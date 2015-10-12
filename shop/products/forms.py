from django import forms
from django.forms import ModelForm
from accounts.models import AuthUser
from .models import ProductReview, Product
from django.shortcuts import get_object_or_404

class ReviewForm(ModelForm):

    class Meta:
        model = ProductReview
        fields = ('score', 'review')
