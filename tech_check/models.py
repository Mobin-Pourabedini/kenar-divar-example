from django.db import models


class User(models.Model):
    phone = models.CharField(max_length=50, primary_key=True)
    access_token = models.CharField(max_length=500)


class Post(models.Model):
    token = models.CharField(max_length=50, primary_key=True)
    code = models.CharField(max_length=255)
    user = models.ForeignKey(User, max_length=50, null=True, on_delete=models.SET_NULL)
    access_token = models.CharField(max_length=500, null=True)


class Technician(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    battery_health = models.IntegerField(default=0)
    screen_health = models.IntegerField(default=0)
    camera_health = models.IntegerField(default=0)
    body_health = models.IntegerField(default=0)
    performance_health = models.IntegerField(default=0)
