# Generated by Django 5.0 on 2024-08-18 15:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("taelimodel", "0010_bannerquote_oursponser"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="banner",
            name="quote",
        ),
    ]
