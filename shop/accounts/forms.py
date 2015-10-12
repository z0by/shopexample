# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from accounts.models import AuthUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Q
from django.core.exceptions import ValidationError


class AuthUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = AuthUser
        fields = ('email', 'username')

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            AuthUser._default_manager.get(username=username)
        except AuthUser.DoesNotExist:
            return username
        raise forms.ValidationError(('Такой пользователь уже существует'), code='duplicate')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AuthUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label='password', help_text='There is no way to see this password.')

    class Meta(UserChangeForm.Meta):
        model = AuthUser
        fields = ('email', 'password', 'is_active', 'is_staff', 'is_superuser', 'user_permissions')

    def clean_password(self):
        return self.initial['password']


class RegistrationForm(forms.Form):
    username = forms.CharField(required=True, label="Username", error_messages={'required': 'Это обязательное поле'})
    email = forms.EmailField(label=("Email"), error_messages={'required': 'Это обязательное поле'})
    phone = forms.CharField(required=False, label="Phone")
    password1 = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput,
                                error_messages={'required': 'Это обязательное поле'})
    password2 = forms.CharField(required=True, label='Подтверждение пароля', widget=forms.PasswordInput,
                                error_messages={'required': 'Это обязательное поле'})

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            AuthUser._default_manager.get(username=username)
        except AuthUser.DoesNotExist:
            return username
        raise forms.ValidationError(('Такой пользователь уже существует'), code='duplicate')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            AuthUser._default_manager.get(email=email)
        except AuthUser.DoesNotExist:
            return email
        raise forms.ValidationError(('Такой email уже существует'), code='duplicate_email')
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone != '':
            try:
                AuthUser._default_manager.get(phone=phone)
            except AuthUser.DoesNotExist:
                return phone
            raise forms.ValidationError(('Такой телефон уже существует'), code='duplicate_phone')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(('Пароли не совпадают'), code='password')
        return password2

    def save(self, commit=False):
        data = self.cleaned_data
        if data['username'] and data['password1']:
            username = data['username']
            email = data['email']
            phone = data['phone']
            password = data['password1']
            customer = AuthUser.objects.create_user(username=username, email=email, phone=phone, password=password,
                                                    is_active=False)
            customer.save()
        return customer


class UpdateUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.prof = kwargs.get('instance', None)
        initial = {'username': self.prof.username, 'email': self.prof.email, 'phone': self.prof.phone,
                   'first_name': self.prof.first_name, 'last_name': self.prof.last_name}
        kwargs['initial'] = initial
        super(UpdateUserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AuthUser
        fields = ('username', 'email', 'phone', 'first_name', 'last_name')


class AuthenticationForm(forms.Form):
    """
    Login form
    """
    username = forms.CharField(required=True, label="Username или Email или телефон")
    password = forms.CharField(widget=forms.widgets.PasswordInput, label="Пароль")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = AuthUser._default_manager.get(Q(username=username) | Q(email=username) | Q(phone=username))
        except AuthUser.DoesNotExist:
            raise forms.ValidationError("Неверный пользователь. Зарегистрируйтесь или укажите верного пользователя")
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = AuthUser._default_manager.get(Q(username=username) | Q(email=username) | Q(phone=username))
        except:
            user = None
        if user is not None and not user.check_password(password):
            raise forms.ValidationError("Неверный пароль")
        elif user is None:
            raise forms.ValidationError("Неверный пользователь или пароль")
        else:
            return password
