# Generated by Django 4.1 on 2024-05-14 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0003_user_alter_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
