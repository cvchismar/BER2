# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Sessions
from django.core.urlresolvers import reverse ##need to import reverse when using named routes!
from django.conf import settings


# Create your views here.



def index(request):
    # print """
    #     VIEWS PAGE
    # """
    return render(request, 'login_app/dashboard.html')

def register(request):
    errors = User.objects.registration_validation(request.POST)
    if len(errors): #there are errors
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        person = User.objects.create(
        name = request.POST['name'],
        l_name = request.POST['l_name'],
        password = request.POST['password'],
        email_address = request.POST['email'])
        request.session['name'] = request.POST['name']
        request.session['id'] = person.id
        return redirect ('/display')

def login(request):
    errors = User.objects.user_validation(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        logged_in_user = User.objects.get(email_address=request.POST['email'])
        print logged_in_user
        request.session['name'] = logged_in_user.name
        request.session['id'] = logged_in_user.id
        return redirect ('/display')

def display(request):
    # Sessions.objects.all().delete()
    context = {
        'users' : User.objects.all(),
        'sessions' : Sessions.objects.filter(created_by=User.objects.get(id=request.session['id'])),
        'other_sessions': Sessions.objects.exclude(created_by=User.objects.get(id=request.session['id']))
    }
    return render(request, 'login_app/index.html', context)

def add_session(request):
    return render(request, 'login_app/add_session.html')

def create(request):
    user = User.objects.get(id=request.session['id'])
    Session = Sessions.objects.create(
        code = request.POST['code'],
        title = request.POST['title'],
        start = request.POST['start'],
        end = request.POST['end'],
        presenter = request.POST['presenter'],
        city = request.POST['city'],
        created_by_id = request.session['id'],
    )
    # session.save()
    return redirect(reverse('users:display'))

def join(request):
    current_user = User.objects.get(id=request.session['id'])
    current_session = Sessions.objects.get(id=sessions_id)
    current_session.joiners.add(current_user)
    current_session.save()
    return redirect('/display')    

def info(request, lecture_id):
    # print "*******************"+ lecture_id + "*******************************************"
    lecture = Sessions.objects.get(id=lecture_id)
    context = {
        'lecture' : lecture
    }

    return render(request, 'login_app/code.html', context)

def billing(request):
    return render(request, 'login_app/billing.html')

def logout(request):
    request.session.clear()
    return redirect('/')