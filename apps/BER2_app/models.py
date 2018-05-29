# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import datetime

# Create your models here.

class UserManager(models.Manager):
    def registration_validation(self, data):
        errors = {}
        if len(data['name']) < 2:
            errors["name"] = "Name needs to be at least 2 characters"

        if len(data['l_name']) < 2:
            errors["l_name"] = "Alias needs to be at least 2 characters"

        if len(data['password']) < 8:
            errors["password"] = "Password needs to be at least 8 characters"
        
        if not data['password'] == data['confirm']:
            errors["password"] = "Passwords do not match"
        return errors

    def user_validation(self,data):
        errors = {}
        
        existing_user = User.objects.filter(email_address = data['email'])

        if len(existing_user) < 1:
            errors["email"] = "Email does not match our records"

        else:
            print existing_user
            print existing_user[0]
            print existing_user[0].password
            if data['password'] != existing_user[0].password:
                errors["password"] = "Password does not match our records for that email"
        return errors



class User(models.Model):
    name= models.CharField(max_length = 255)
    l_name = models.CharField(max_length = 255)
    email_address = models.CharField(max_length = 255, unique = True)
    password = models.CharField(max_length = 255)
    
    objects = UserManager()





class Sessions(models.Model):
    created_by = models.ForeignKey(User, related_name = "created_by")
    # joiner = models.ManyToManyField(User, related_name = "joined_by")
    code = models.CharField(max_length = 255)
    title = models.CharField(max_length = 255)
    presenter = models.CharField(max_length = 255)
    start = models.DateField()
    end = models.DateField()
    city = models.CharField(max_length = 255, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # objects = SessionsManager()
def attendees(self):
    return self.joined_by.exclude(id=self.created_by.id)
