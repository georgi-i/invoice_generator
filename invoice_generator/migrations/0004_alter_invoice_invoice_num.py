# Generated by Django 3.2.6 on 2021-08-30 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_generator', '0003_rename_number_invoice_invoice_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_num',
            field=models.IntegerField(),
        ),
    ]