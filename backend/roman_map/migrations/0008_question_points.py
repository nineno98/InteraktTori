# Generated by Django 4.2.18 on 2025-02-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roman_map', '0007_quiz_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
