# Generated by Django 4.1.4 on 2023-01-11 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('replays', '0021_alter_replaystage_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='replay',
            name='slowdown',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
