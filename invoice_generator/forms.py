from django import forms

class InvoiceForm(forms.Form):
    date = forms.DateInput()
    invoice_num = forms.NumberInput()
    company_id = forms.NumberInput()
    company_name = forms.CharField()
    company_city = forms.CharField()
    company_address = forms.CharField()
    company_manager = forms.CharField()
    place = forms.CharField()
    product_name = forms.CharField()
    quantity = forms.FloatField()
    measure = forms.CharField()
    unit_price = forms.FloatField()
    value = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].required = False
        self.fields['quantity'].required = False
        self.fields['measure'].required = False
        self.fields['unit_price'].required = False
        self.fields['value'].required = False

class SearchForm(forms.Form):
    keyword = forms.CharField()

