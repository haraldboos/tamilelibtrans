# Generated by Django 5.0 on 2024-12-17 15:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taelimodel", "0021_alter_impresm_options"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StripPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cart",
            name="payment_intent_id",
            field=models.CharField(
                blank=True,
                help_text="Used to track Stripe Payment Intents",
                max_length=255,
                null=True,
                verbose_name="Stripe Payment Intent ID",
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="stripe_customer_id",
            field=models.CharField(
                blank=True,
                help_text="Optional field for Stripe customer tracking",
                max_length=255,
                null=True,
                verbose_name="Stripe Customer ID",
            ),
        ),
        migrations.AddConstraint(
            model_name="cart",
            constraint=models.UniqueConstraint(
                fields=("user", "bookno", "booklang"), name="unique_cart_item"
            ),
        ),
    ]