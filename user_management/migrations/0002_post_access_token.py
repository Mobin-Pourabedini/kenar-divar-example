# Generated by Django 4.1 on 2024-05-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='access_token',
            field=models.CharField(max_length=500, null=True),
        ),
    ]