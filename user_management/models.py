from django.db import models


class Post (models.Model):
    token = models.CharField(max_length=50, primary_key=True)
    code = models.CharField(max_length=255)
    user = models.CharField(max_length=50, null=True)
    access_token = models.CharField(max_length=500, null=True)
