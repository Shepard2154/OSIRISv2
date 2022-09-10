# Generated by Django 3.2.13 on 2022-09-10 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('special', '0006_auto_20220510_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveCeleryTasks',
            fields=[
                ('name', models.CharField(max_length=1000, primary_key=True, serialize=False)),
                ('task_id', models.CharField(max_length=5000)),
                ('entities', models.TextField()),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'db_table': 'active_celery_tasks',
            },
        ),
    ]
