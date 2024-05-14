from django.db import models

from user_management.models import Post


class Technician(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class Report(models.Model):
    post_token = models.ForeignKey(Post, on_delete=models.CASCADE)
    technician_id = models.ForeignKey(Technician, on_delete=models.CASCADE)
    battery_health = models.IntegerField(default=0)
    screen_health = models.IntegerField(default=0)
    camera_health = models.IntegerField(default=0)
    body_health = models.IntegerField(default=0)
    performance_health = models.IntegerField(default=0)
