# Generated by Django 3.2.13 on 2022-05-10 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('special', '0005_auto_20220509_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='category',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='location',
            field=models.CharField(blank=True, default='', max_length=2500, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='web',
            field=models.CharField(blank=True, default='', max_length=2500, null=True),
        ),
    ]
