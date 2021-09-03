from rest_framework import serializers

from invoice_generator.models import Invoice, Product, Tax


class TaxSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tax
        fields = ('tax_base', 'tax_rate', 'payment_amount')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'quantity', 'measure', 'unit_price', 'value')
    

class InvoiceSerializer(serializers.ModelSerializer):

    products = ProductSerializer(many=True)
    tax = TaxSerializer()

    class Meta:
        model = Invoice
        fields = ('invoice_num', 'date', 'company_id', 'company_name', 'company_city', 
                    'company_address', 'company_manager' ,'place', 'products', 'tax')


    def create(self, validated_data):

        invoice_data = validated_data.pop('products')
        tax_data = validated_data.pop('tax')

        invoice = Invoice.objects.create(**validated_data)
        Tax.objects.create(invoice=invoice, **tax_data)
        
        for product_data in invoice_data:
            Product.objects.create(invoice=invoice, **product_data)
        
        return invoice

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products')
        products = list((instance.products).all())
        instance.invoice_num = validated_data.get('invoice_num', instance.invoice_num)
        instance.date = validated_data.get('date', instance.date)
        instance.company_id = validated_data.get('company_id', instance.company_id)
        instance.place = validated_data.get('place', instance.place)
        instance.save()
        for product_data in products_data:
            product = Product(invoice_id=instance.id)
            if len(products) > 0:
                product = products.pop(0)
            product.name = product_data.get('name', product.name)
            product.quantity = product_data.get('quantity', product.quantity)
            product.measure = product_data.get('measure', product.measure)
            product.unit_price = product_data.get('unit_price', product.unit_price)
            product.value = product_data.get('value', product.value)
            product.save()
        
        instance.save()

        return instance


        
        
