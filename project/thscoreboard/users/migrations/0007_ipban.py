# Generated by Django 4.1 on 2022-12-25 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_visits'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPBan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.TextField()),
            ],
        ),
    ]
