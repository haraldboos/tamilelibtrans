# Generated by Django 5.0 on 2024-10-04 11:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taelimodel", "0017_alter_adminstration_ocation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="projects",
            name="gbid",
            field=models.CharField(
                blank=True,
                max_length=255,
                verbose_name="the id for every file from google drive",
            ),
        ),
    ]