# Generated by Django 3.2.7 on 2022-01-17 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osiris', '0019_alter_twittertweet_original_screen_name'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='twitteruserinfo',
            table='twitter_userinfo',
        ),
    ]
