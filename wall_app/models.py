from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name'] = "First name must be 2 or more characters!"
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name must be 2 or more characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password'])<8:
            errors['password'] = "Password must be 8 or more characters!"
        if postData['password'] != (postData['password2']):
            errors['password_match'] = "Passwords do not match!"
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['email_dup'] = "Email Already Exists!"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length =255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User,related_name = 'message',on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comments(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message,related_name = 'comment',on_delete = models.CASCADE)
    user = models.ForeignKey(User,related_name = 'comment',on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)