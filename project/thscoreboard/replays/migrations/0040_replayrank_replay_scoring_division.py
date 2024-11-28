# Generated by Django 4.2.4 on 2024-08-18 22:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("replays", "0039_replaystage_th128_frozen_area"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReplayRank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "db_table": "replays_rank",
                "managed": False,
            },
        ),
        migrations.AddIndex(
            model_name="replay",
            index=models.Index(
                fields=[
                    "replay_type",
                    "shot_id",
                    "difficulty",
                    "route_id",
                    "category",
                    "-score",
                ],
                name="scoring_division",
            ),
        ),
    ]