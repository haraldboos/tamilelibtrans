# Generated by Django 5.0.3 on 2024-05-07 16:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taelimodel", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="books",
            name="bookdiscrib_it",
            field=models.CharField(
                max_length=1000, null=True, verbose_name="Discribe Book"
            ),
        ),
        migrations.AddField(
            model_name="books",
            name="bookname_it",
            field=models.CharField(
                max_length=40, null=True, verbose_name="Enter Book Name"
            ),
        ),
        migrations.AddField(
            model_name="catagory",
            name="catagoryname_it",
            field=models.CharField(
                max_length=50, null=True, verbose_name="Enter Catagory Name"
            ),
        ),
    ]