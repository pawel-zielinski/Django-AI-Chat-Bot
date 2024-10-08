# Generated by Django 5.1.1 on 2024-10-01 19:45

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
        migrations.AlterField(
            model_name="message",
            name="session",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.chatsession",
            ),
        ),
        migrations.DeleteModel(
            name="QuestionAnswer",
        ),
    ]