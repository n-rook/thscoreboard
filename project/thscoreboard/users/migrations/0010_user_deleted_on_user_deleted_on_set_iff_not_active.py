# Generated by Django 4.1.4 on 2023-02-09 17:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_alter_ban_reason"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="deleted_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("deleted_on__isnull", False), ("is_active", False)),
                    models.Q(("deleted_on__isnull", True), ("is_active", True)),
                    _connector="OR",
                ),
                name="deleted_on_set_iff_not_active",
            ),
        ),
    ]
