# Generated by Django 3.2.13 on 2022-05-09 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('special', '0004_auto_20220502_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
