from django.db import models

class Invoice(models.Model):
    invoice_num = models.IntegerField()
    date = models.DateField()
    company_id = models.IntegerField()
    company_name = models.CharField(max_length=50, blank=True, null=True)
    company_city = models.CharField(max_length=20, blank=True, null=True)
    company_address = models.CharField(max_length=100, blank=True, null=True)
    company_manager = models.CharField(max_length=85, blank=True, null=True)
    place = models.CharField(max_length=30) 

    def __int__(self):
        return self.invoice_num

class Product(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    measure = models.CharField(max_length=12, blank=True, null=True)
    unit_price = models.FloatField(max_length=7, blank=True, null=True)
    value = models.FloatField(max_length=8, blank=True, null=True)

class Tax(models.Model):
    invoice = models.OneToOneField(Invoice, related_name='tax', on_delete=models.CASCADE, blank=True, null=True)
    tax_base = models.FloatField(max_length=10, blank=True, null=True)
    tax_rate = models.FloatField(max_length=10, blank=True, null=True)
    payment_amount = models.FloatField(max_length=12, blank=True, null=True)
    
