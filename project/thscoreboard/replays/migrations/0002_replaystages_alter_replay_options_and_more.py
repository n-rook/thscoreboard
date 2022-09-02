# Generated by Django 4.1 on 2022-09-02 15:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('replays', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplayStages',
            fields=[
                ('replay', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='replays.replay')),
                ('stage', models.IntegerField()),
                ('power', models.IntegerField(blank=True, null=True)),
                ('piv', models.IntegerField(blank=True, null=True)),
                ('lives', models.IntegerField(blank=True, null=True)),
                ('life_pieces', models.IntegerField(blank=True, null=True)),
                ('bombs', models.IntegerField(blank=True, null=True)),
                ('bomb_pieces', models.IntegerField(blank=True, null=True)),
                ('graze', models.IntegerField(blank=True, null=True)),
                ('point_items', models.IntegerField(blank=True, null=True)),
                ('th06_rank', models.IntegerField(blank=True, null=True)),
                ('th07_cherry', models.IntegerField(blank=True, null=True)),
                ('th07_cherrymax', models.IntegerField(blank=True, null=True)),
                ('th08_time', models.IntegerField(blank=True, null=True)),
                ('th08_human_youkai', models.IntegerField(blank=True, null=True)),
                ('th09_char', models.IntegerField(blank=True, null=True)),
                ('th09_ai', models.IntegerField(blank=True, null=True)),
                ('th12_ufo1', models.IntegerField(blank=True, null=True)),
                ('th12_ufo2', models.IntegerField(blank=True, null=True)),
                ('th12_ufo3', models.IntegerField(blank=True, null=True)),
                ('th125_freeze_area', models.IntegerField(blank=True, null=True)),
                ('extends', models.IntegerField(blank=True, null=True)),
                ('th13_trance', models.IntegerField(blank=True, null=True)),
                ('th14_poc_count', models.IntegerField(blank=True, null=True)),
                ('th14_miss_count', models.IntegerField(blank=True, null=True)),
                ('th16_season', models.IntegerField(blank=True, null=True)),
                ('th17_hyper_fill', models.IntegerField(blank=True, null=True)),
                ('th17_token1', models.IntegerField(blank=True, null=True)),
                ('th17_token2', models.IntegerField(blank=True, null=True)),
                ('th17_token3', models.IntegerField(blank=True, null=True)),
                ('th17_token4', models.IntegerField(blank=True, null=True)),
                ('th17_token5', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='replay',
            options={'ordering': ['shot', 'difficulty', '-score']},
        ),
        migrations.RenameField(
            model_name='replay',
            old_name='points',
            new_name='score',
        ),
        migrations.RemoveField(
            model_name='replayfile',
            name='points',
        ),
        migrations.AddField(
            model_name='replay',
            name='clear',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='replay',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 3, 1, 21, 6, 91406)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='replay',
            name='name',
            field=models.TextField(default='tempname'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='replay',
            name='rep_score',
            field=models.BigIntegerField(default=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='replay',
            name='slowdown',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='replay',
            name='spellpracticeid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='replay',
            name='video_link',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddConstraint(
            model_name='replaystages',
            constraint=models.UniqueConstraint(models.F('replay'), models.F('stage'), name='unique_stage_per_replay'),
        ),
    ]
