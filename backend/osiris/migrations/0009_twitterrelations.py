# Generated by Django 3.2.7 on 2022-01-15 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('osiris', '0008_delete_twitterrelations'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterRelations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower_id', models.PositiveIntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osiris.twitteruserinfo')),
            ],
            options={
                'db_table': 'twitter_relations',
                'unique_together': {('user_id', 'follower_id')},
            },
        ),
    ]
