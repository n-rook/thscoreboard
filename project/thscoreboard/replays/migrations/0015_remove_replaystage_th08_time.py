# Generated by Django 4.1 on 2022-12-05 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replays', '0014_replaystage_th08_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replaystage',
            name='th08_time',
        ),
    ]