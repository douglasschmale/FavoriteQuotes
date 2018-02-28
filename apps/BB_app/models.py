from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class Registercheck(models.Manager):
    def regvalidator(self, postData):
        current_user = Users.objects.filter(email=postData['email'].lower())
        errors = []
        if len(postData['first']) < 1:
            errors.append("First name field can not be blank.")
        elif not NAME_REGEX.match(postData['first']):
            errors.append("First name must contain only letters.")

        if len(postData['last']) < 1:
            errors.append("Last name field can not be blank.")
        elif not NAME_REGEX.match(postData['last']):
            errors.append("Last name must contain only letters.")

        if len(postData['email']) < 1:
            errors.append("Email field cannot be blank")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email")
        elif len(current_user) > 0:
            errors.append("Email already exists")

        if len(postData['password']) < 8:
            errors.append("Password must be at least eight characters.")
        elif (postData["password"] != postData["confirm"]):
            errors.append("Password confirmation must match password.")

        if len(postData["birthday"]) < 1:
            errors.append("Date of Birth is required")
        else:
            dob = datetime.strptime(postData["birthday"], "%Y-%m-%d")
            if dob > datetime.now():
                errors.append("You must have been born in the past to register!")
        return errors

    def loginvalidator(self, postData):
        current_user = Users.objects.filter(email=postData['email'].lower())
        print current_user
        error = []
        if len(postData['email']) < 1:
            error.append("Email field cannot be blank")
        elif not EMAIL_REGEX.match(postData['email']):
            error.append("Invalid email")
        elif not (current_user):
            error.append("Email not recognized. Please register.")

        elif len(postData['password']) < 8:
            error.append("Password must be at least eight characters.")
        elif not bcrypt.checkpw(postData["password"].encode(), current_user[0].password.encode()):
            error.append("Incorrect Password.")

        return error

class itemCheck(models.Manager):
    def validator(self, postData):
        errors = []
        if len(postData['product']) < 1:
            errors.append("Product name field can not be blank.")
        elif len(postData['product']) < 3:
            errors.append("Product name must be at least 3 characters.")
        return errors

class Users(models.Model):
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    objects = Registercheck()

class Items(models.Model):
    product = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    creator = models.ForeignKey(Users, related_name="user_item")
    favorite = models.ManyToManyField(Users, related_name="user_favorite")
    objects = itemCheck()
