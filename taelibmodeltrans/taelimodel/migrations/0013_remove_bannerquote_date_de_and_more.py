# Generated by Django 5.0 on 2024-08-18 15:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("taelimodel", "0012_bannerquote_date_de_bannerquote_date_en_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bannerquote",
            name="date_de",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="date_en",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="date_fr",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="date_it",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="date_si",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="date_ta",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="status_de",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="status_en",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="status_fr",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="status_it",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="status_si",
        ),
        migrations.RemoveField(
            model_name="bannerquote",
            name="status_ta",
        ),
    ]
