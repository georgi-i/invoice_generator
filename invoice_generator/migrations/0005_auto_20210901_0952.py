# Generated by Django 3.2.6 on 2021-09-01 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_generator', '0004_alter_invoice_invoice_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='company_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='company_city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='company_manager',
            field=models.CharField(blank=True, max_length=85, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='company_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
