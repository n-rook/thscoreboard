# Generated by Django 4.1 on 2022-10-22 18:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_unverifieduser_alter_userpasscodetie_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unverifieduser',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
