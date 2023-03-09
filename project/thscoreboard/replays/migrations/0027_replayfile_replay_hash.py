# Generated by Django 4.1.4 on 2023-03-09 10:35

from django.db import migrations, models
import hashlib


class Migration(migrations.Migration):

    dependencies = [
        ('replays', '0026_merge_20230221_1947'),
    ]

    def alter_replayfile_replayhash_calculate_value(apps, _):
        replay_file = apps.get_model('replays', 'replayfile')
        rf = replay_file.objects.all()
        for r in rf:
            h = hashlib.sha256(r.replay_file)
            r.replay_hash = h.digest()
            r.save()


    def alter_replayfile_replayhash_calculate_value_undo(apps, _):
        replay_file = apps.get_model('replays', 'replayfile')
        rf = replay_file.objects.all()
        for r in rf:
            r.replay_hash = 0
            r.save()


    operations = [
        migrations.AddField(
            model_name='replayfile',
            name='replay_hash',
            field=models.BinaryField(null=True, max_length=32),
        ),
        migrations.RunPython(alter_replayfile_replayhash_calculate_value, alter_replayfile_replayhash_calculate_value_undo),
        migrations.AlterField(
            model_name='replayfile',
            name='replay_hash',
            field=models.BinaryField(null=False, max_length=32)
        ),
        migrations.AddConstraint(
            model_name='replayfile',
            constraint=models.UniqueConstraint(fields=('replay_hash',), name='unique_hash'),
        )
    ]
