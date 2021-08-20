from rest_framework import viewsets

from invoice_generator.serializers import InvoiceSerializer
from invoice_generator.models import Invoice

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

