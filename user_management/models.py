from django.db import models

class Post (models.Model):
    token = models.CharField(max_length=50)
