# Generated by Django 4.1.4 on 2022-12-16 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('replays', '0016_replaystage_th09_p1_cpu_replaystage_th09_p2_cpu_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='replay',
            name='spell_card_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
