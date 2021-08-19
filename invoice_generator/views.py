from rest_framework import viewsets

from invoice_generator.serializers import InvoiceSerializer, ProductSerializer, TaxSerializer
from invoice_generator.models import Invoice

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

class TaxViewSet(viewsets.ModelViewSet):
    serializer_class = TaxSerializer
