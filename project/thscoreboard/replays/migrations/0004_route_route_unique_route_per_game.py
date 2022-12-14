# Generated by Django 4.1 on 2022-09-18 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('replays', '0003_replay_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_id', models.TextField()),
                ('order_number', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='replays.game')),
            ],
        ),
        migrations.AddConstraint(
            model_name='route',
            constraint=models.UniqueConstraint(models.F('route_id'), models.F('game'), name='unique_route_per_game'),
        ),
    ]
