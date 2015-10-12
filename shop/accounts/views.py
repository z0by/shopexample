# -*- coding: utf-8 -*-
import hashlib
import datetime
import random
from models import AuthUser
from forms import RegistrationForm, UpdateUserForm,AuthenticationForm
from django.shortcuts import render, render_to_response, get_object_or_404, Http404
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as django_login, authenticate
from django.template import RequestContext
from django.contrib import messages
from django.conf import settings

def register_user(request):

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            if new_user.email:
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                new_user.activation_key = hashlib.sha1(salt+new_user.email).hexdigest()
                new_user.key_expires = datetime.datetime.today() + datetime.timedelta(2)
                new_user.save()
                # Send email with activation key
                email_subject = u'Подтверждение '
                email_body = u"Добро пожаловать в магазин, %s. Спасибо за регистрацию. Чтобы активировать аккаунт, перейди по ссылке \
                 %s/account/confirm/%s" % (new_user.username,settings.SITE_URL, new_user.activation_key)

                send_mail(email_subject, email_body, 'sendmail@z0.by',
                    [new_user.email], fail_silently=False)

                return HttpResponseRedirect('/account/registersuccess')

            elif new_user.phone:
                new_user.save()
                return HttpResponseRedirect('/account')
            else:
                return HttpResponseRedirect('/')
        else:
            print form.errors
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        HttpResponseRedirect('/')
    user = get_object_or_404(AuthUser, activation_key=activation_key)
    if user.is_active:
        raise Http404

    if user.key_expires < timezone.now():
        return render_to_response('accounts/confirm_expired.html')


    user.is_active = True
    user.save()
    return render_to_response('accounts/confirm.html')

@login_required(login_url='/account/login/')
def edit_profile(request):
    user_profile =  request.user
    #form = UpdateProfileForm(instance=user_profile)
    if request.POST:
        form = UpdateUserForm(request.POST,instance=user_profile)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect('/account/edit')
        else:
            return HttpResponseRedirect('/')

    form = UpdateUserForm(instance=user_profile)

    return render(request, 'accounts/edit.html', {'form': form})


def login_user(request):
    next = request.GET.get('next')
    form = AuthenticationForm()
    if request.method == 'POST':
        print 1
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print 2
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                print 3
                if user.is_active:
                        print 4
                        django_login(request, user)
                        if next:

                            return HttpResponseRedirect(next)
                        else:
                            return HttpResponseRedirect(next)
                else:

                    messages.error(request, "Нет такого пользователя или он не активирован!")
            else:

                 messages.error(request, "Неверный пользователь или пароль!")





    return render_to_response('accounts/login.html', {
         'form': form,
         }, context_instance=RequestContext(request))

def register_success(request):

     return render_to_response('accounts/register_success.html', {}, context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.delete_cookie('petsshopcart')
    return response