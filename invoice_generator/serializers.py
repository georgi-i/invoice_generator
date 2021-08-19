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
        fields = ('number', 'date', 'company_id', 'place', 'products', 'tax')

    
    def create(self, validated_data):

        invoice_data = validated_data.pop('products')
        tax_data = validated_data.pop('tax')

        invoice = Invoice.objects.create(**validated_data)
        Tax.objects.create(invoice=invoice, **tax_data)
        
        for product_data in invoice_data:
            Product.objects.create(invoice=invoice, **product_data)
        
        return invoice

    def update(self, instance, validated_data):
            instance.number = validated_data.get('number', instance.number)
            instance.date = validated_data.get('date', instance.date)
            instance.company_id = validated_data.get('company_id', instance.company_id)
            instance.place = validated_data.get('place', instance.place)
            instance.products

            #prod_dict = validated_data.get('products', instance.products)
            #prod_instances = []
            #for dict in prod_dict:
            #    prod_instance = Product(name=dict['name'], 
            #                        quantity=dict['quantity'], 
            #                        measure=dict['measure'],
            #                        unit_price=dict['unit_price'],
            #                        value=dict['value'])

                #prod_instances.append(prod_instance)
            
            invoice_data = validated_data.pop('products')
            tax_data = validated_data.pop('tax')
            invoice = Invoice.objects.create(**validated_data)
            Tax.objects.create(invoice=invoice, **tax_data)

            for product_data in invoice_data:
                instance.products.set([Product.objects.create(invoice=invoice, **product_data)])
                
            #instance.products.set(prod_instances)

            #tax_dict = validated_data.get('tax', instance.tax)
            #tax_instance = Tax(tax_base=tax_dict['tax_base'], 
            #                    tax_rate=tax_dict['tax_rate'], 
            #                    payment_amount=tax_dict['payment_amount'])
                                
            #instance.tax = tax_instance
            #instance.save()

            return instance


        
        
