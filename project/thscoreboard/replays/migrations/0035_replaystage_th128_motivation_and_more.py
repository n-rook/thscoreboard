# Generated by Django 4.1.6 on 2023-05-20 09:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("replays", "0034_alter_replay_category_alter_replay_replay_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="replaystage",
            name="th128_motivation",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="replaystage",
            name="th128_perfect_freeze",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
