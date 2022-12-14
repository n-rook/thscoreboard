# Generated by Django 4.1 on 2022-08-30 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.TextField(primary_key=True, serialize=False)),
                ('has_replays', models.BooleanField()),
                ('num_difficulties', models.IntegerField()),
            ],
            options={
                'ordering': ['game_id'],
            },
        ),
        migrations.CreateModel(
            name='Replay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[(1, 'Regular'), (2, 'Tas'), (3, 'Unlisted'), (4, 'Private')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('difficulty', models.IntegerField()),
                ('points', models.BigIntegerField()),
                ('video_link', models.TextField(max_length=1000)),
                ('comment', models.TextField(max_length=50000)),
            ],
            options={
                'ordering': ['shot', 'difficulty', '-points'],
            },
        ),
        migrations.CreateModel(
            name='TemporaryReplayFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('replay', models.BinaryField(max_length=1000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shot_id', models.TextField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='replays.game')),
            ],
        ),
        migrations.CreateModel(
            name='ReplayFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replay_file', models.BinaryField(blank=True, max_length=1000000, null=True)),
                ('is_good', models.BooleanField()),
                ('points', models.BigIntegerField()),
                ('replay', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='replays.replay')),
            ],
        ),
        migrations.AddField(
            model_name='replay',
            name='shot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='replays.shot'),
        ),
        migrations.AddField(
            model_name='replay',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='shot',
            constraint=models.UniqueConstraint(models.F('shot_id'), models.F('game'), name='unique_shot_per_game'),
        ),
        migrations.AddConstraint(
            model_name='replay',
            constraint=models.CheckConstraint(check=models.Q(('difficulty__gte', 0)), name='difficulty_gte_0'),
        ),
    ]
