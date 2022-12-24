# Generated by Django 4.1.2 on 2022-12-11 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_follow_followed_follow_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='followers_follow',
        ),
        migrations.AlterField(
            model_name='follow',
            name='user_follow',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_who_follow', to=settings.AUTH_USER_MODEL),
        ),
    ]
