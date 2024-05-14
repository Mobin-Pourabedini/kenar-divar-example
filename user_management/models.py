from django.db import models


class Post (models.Model):
    token = models.CharField(max_length=50, primary_key=True)
    code = models.CharField(max_length=255)
    user = models.ForeignKey('user_management.User', max_length=50, null=True, on_delete=models.SET_NULL)
    access_token = models.CharField(max_length=500, null=True)


class User (models.Model):
    phone = models.CharField(max_length=50, primary_key=True)
    access_token = models.CharField(max_length=500)
