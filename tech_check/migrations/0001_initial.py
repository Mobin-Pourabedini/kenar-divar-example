# Generated by Django 4.1 on 2024-05-14 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management', '0004_user_access_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery_health', models.IntegerField(default=0)),
                ('screen_health', models.IntegerField(default=0)),
                ('camera_health', models.IntegerField(default=0)),
                ('body_health', models.IntegerField(default=0)),
                ('performance_health', models.IntegerField(default=0)),
                ('post_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.post')),
                ('technician_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tech_check.technician')),
            ],
        ),
    ]