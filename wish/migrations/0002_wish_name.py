# Generated by Django 4.2 on 2024-11-21 04:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wish", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="wish",
            name="name",
            field=models.CharField(default=1, max_length=100, verbose_name="Название"),
            preserve_default=False,
        ),
    ]
