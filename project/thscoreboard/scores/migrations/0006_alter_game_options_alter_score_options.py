# Generated by Django 4.1 on 2022-08-19 00:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0005_replayfile_replay'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['game_id']},
        ),
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ['shot', 'difficulty', '-points']},
        ),
    ]