from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime
NAME_REGEX = re.compile(r'^[A-Za-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  def reg_validator(self,postData):
    errors = {}
    if "name" not in postData or len(postData['name']) < 3:
      errors['name'] = "Name need to more than 3 characters"
    if "username" not in postData or len(postData['username']) < 3:
      errors['username'] = "Username need to more than 3 characters"
    if 'password' not in postData or len(postData['password'])<8:
      errors['password'] = "Password must have at least 8 characters"
    if "confirm" not in postData or postData['password'] != postData['confirm']:
      errors['password'] = "Please enter your password again"
    if "date_hired" not in postData or postData['date_hired'] < 1:
      errors['date_hired'] = "Please enter your hired date."
    if not len(errors):
      users = User.objects.filter(username = postData['username'])
      if users:
        errors['username'] = "Please enter a valid username"
    return errors

  def login_check(self,postData):
    error = {}
    users = User.objects.filter(username = postData['username'])
    if not users or not bcrypt.checkpw(postData['password'].encode(),users[0].password.encode()):
      error['login'] = "Email and password not match"
    return error

class ItemManager(models.Manager):
  def item_check(self,postData):
    errors = {}
    if len(postData['item']) < 3:
      errors['item'] = "Please item name should more than 3 characters."
    return errors

class User(models.Model):
  name = models.CharField(max_length=255)
  username = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  date_hire = models.DateTimeField(auto_now_add=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()
  def __str__(self):
           return self.name

class Item(models.Model):
  item_name = models.CharField(max_length=255)
  creater = models.ForeignKey(User, related_name = "createitems")
  follower = models.ManyToManyField(User, related_name = "followitems")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = ItemManager()
  def __str__(self):
           return self.item_name








