from django.db import models

class Rating (models.Model):
    post_token = models.CharField(max_length=50)
    text = models.CharField(max_length=255)
    rate = models.IntegerField(default=0)
    demand_id = models.ForeignKey('divar_homepage.DivarProfile', on_delete=models.CASCADE, related_name='demand')
    supplier_id = models.ForeignKey('divar_homepage.DivarProfile', on_delete=models.CASCADE, related_name='supplier')
