# Generated by Django 3.2.5 on 2021-07-25 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_account', '0004_profile_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image_url',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
