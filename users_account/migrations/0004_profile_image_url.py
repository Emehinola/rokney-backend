# Generated by Django 3.2.5 on 2021-07-25 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_account', '0003_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
