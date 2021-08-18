from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=120)
    quantity = models.IntegerField()
    measure = models.CharField(max_length=12)
    unit_price = models.FloatField(max_length=7)
    value = models.FloatField(max_length=8)
    pass

class Tax(models.Model):
    tax_base = models.FloatField(max_length=10)
    tax_rate = models.FloatField(max_length=10)
    payment_amount = models.FloatField(max_length=12)
    pass

class Invoice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    number = models.IntegerField()
    date = models.DateField()
    company_id = models.IntegerField()
    place = models.CharField(max_length=30)    
    
    def __str__(self):
        return self.number
