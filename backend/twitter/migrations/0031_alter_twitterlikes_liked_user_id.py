# Generated by Django 3.2.13 on 2022-04-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0030_twitterlikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterlikes',
            name='liked_user_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
