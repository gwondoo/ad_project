# Generated by Django 5.1.5 on 2025-06-15 13:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pybo", "0006_auto_20200507_1449"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="answer",
            name="voter",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="modify_date",
        ),
        migrations.RemoveField(
            model_name="question",
            name="voter",
        ),
        migrations.AlterField(
            model_name="answer",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="create_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
