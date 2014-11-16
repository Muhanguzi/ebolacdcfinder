from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User

from user_account.forms import RegistrationForm
from user_profile.models import UserProfile

import hashlib, datetime, random


def register_user(request):
    if request.user.is_authenticated():
        return HttpResponse(content="Forbidden", status=403)
    else:
        args = {}
        args.update(csrf(request))
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            args['form'] = form
            if form.is_valid(): 
                form.save()  # save user to database if form is valid

                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
                activation_key = hashlib.sha1(salt+email).hexdigest()            
                key_expires = datetime.datetime.today() + datetime.timedelta(2)

                #Get user by username
                user=User.objects.get(username=username)

                # Create and save user profile                                                                                                                                 
                new_profile = UserProfile(user=user, activation_key=activation_key, 
                    key_expires=key_expires)
                new_profile.save()

                # Send email with activation key
                email_subject = 'User account confirmation'
                email_body = "Hello, %s, thank you for creating your profile! \
                To activate your profile please open this link within next 48h \
                http://127.0.0.1:8000/user-account/submit/%s" % (username, activation_key)

                send_mail(email_subject, email_body, 'zadar.events@gmail.com',
                    [email], fail_silently=False)

                return HttpResponseRedirect('/user-account/account-successfully-created')
        else:
            args['form'] = RegistrationForm()

        return render_to_response('user_account/register.html', args, context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        return HttpResponse(content="Forbidden", status=403)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    if user_profile.key_expires < timezone.now():
        return render_to_response('user_account/confirm_expired.html')
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('user_account/confirm.html', context_instance=RequestContext(request))


def register_success(request):
    return render_to_response('user_account/register_success.html', context_instance=RequestContext(request))

# ----------------------------------------------

# AUTHENTICATION
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return render_to_response('user_account/login.html', context_instance=RequestContext(request))

def invalid_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return render_to_response('user_account/invalid_login.html', context_instance=RequestContext(request))


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)


    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/user-account/profile/%s' %(request.user.username))
        else:
            return HttpResponse("It looks like you still haven't verified your email address. \
                Please check your email and open verification link.")
    else:
        return HttpResponseRedirect('/user-account/error')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def forgot_password(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return render_to_response('user_account/forgot_password.html', context_instance=RequestContext(request))


from django.contrib.auth.views import password_reset as real_password_reset
def password_reset(request, *args, **kwargs):
    if request.user.is_authenticated():
       return HttpResponseRedirect('/')
    return real_password_reset(request, *args, **kwargs)


    

