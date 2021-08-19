from django.db import models

class Invoice(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    company_id = models.IntegerField()
    place = models.CharField(max_length=30) 

    def __str__(self):
        return f'{self.number}'

class Product(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    quantity = models.IntegerField()
    measure = models.CharField(max_length=12)
    unit_price = models.FloatField(max_length=7)
    value = models.FloatField(max_length=8)

    def __str__(self):
        return self.name

class Tax(models.Model):
    invoice = models.OneToOneField(Invoice, related_name='tax', on_delete=models.CASCADE)
    tax_base = models.FloatField(max_length=10)
    tax_rate = models.FloatField(max_length=10)
    payment_amount = models.FloatField(max_length=12)
    
    def __str__(self):
        return f'{self.invoice}'
