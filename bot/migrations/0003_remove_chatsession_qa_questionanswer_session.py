# Generated by Django 5.1.1 on 2024-09-27 20:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0002_message"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatsession",
            name="qa",
        ),
        migrations.AddField(
            model_name="questionanswer",
            name="session",
            field=models.ForeignKey(
                default=1,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.chatsession",
            ),
        ),
    ]
