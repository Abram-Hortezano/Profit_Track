# Generated by Django 4.2.5 on 2023-10-22 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_category_paymentmethod_recordtransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recordtransaction',
            name='actions',
        ),
    ]
