# Generated by Django 4.1 on 2024-05-14 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('token', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
