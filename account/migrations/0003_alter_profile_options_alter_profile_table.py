# Generated by Django 5.0.7 on 2024-08-05 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_subscription_profile_followers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'профиль', 'verbose_name_plural': 'профили'},
        ),
        migrations.AlterModelTable(
            name='profile',
            table='profile',
        ),
    ]
