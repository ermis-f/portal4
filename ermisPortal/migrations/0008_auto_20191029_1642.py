# Generated by Django 2.1 on 2019-10-29 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ermisPortal', '0007_user_cr_is_editor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]