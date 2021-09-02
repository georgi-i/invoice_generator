from invoice_generator.models import Invoice
from django import forms

class InvoiceForm(forms.Form):
    date = forms.DateInput()
    invoice_num = forms.NumberInput()
    company_id = forms.NumberInput()
    company_name = forms.CharField()
    company_city = forms.CharField()
    company_address = forms.CharField()
    company_manager = forms.CharField()
    place = forms.CharField(required=False, initial='София')
    product_name = forms.CharField()
    quantity = forms.NumberInput()
    measure = forms.CharField()
    unit_price = forms.FloatField()
    value = forms.FloatField()

    class Meta:
        exclude = ('product_name', 'quantity', 'measure', 'unit_price', 'value')


