from rest_framework import viewsets
from django.views.generic import TemplateView
from .forms import InvoiceForm, SearchForm
from django.shortcuts import render
from .post import check_company_id, handle_request, invoice_search


from invoice_generator.serializers import InvoiceSerializer
from invoice_generator.models import Invoice

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class HomeView(TemplateView):

    template_name = "invoice_generator/form.html"
    form_class = InvoiceForm

    def post(self, request, *args, **kwargs):

        if "check_company_id" in request.POST:
            data = check_company_id(request)
            
            return render(request, "invoice_generator/form.html", { 'company_data': data['company_data'], 
                                                                    'company_id': data['company_id'],
                                                                    'invoice_num': data['invoice_num'], 
                                                                    'date': data['date'],
                                                                    'place': data['place'] })

        form = self.form_class(request.POST)
        if form.is_valid():
                        
            data = handle_request(request, form.data)

            return render(request, "invoice_generator/form.html", { 'products': data['products'], 
                                                                    'invoice_num': data['invoice_num'], 
                                                                    'date': data['date'],
                                                                    'company_id': data['company_id'],
                                                                    'company_data': data['company_data'],
                                                                    'place': data['place'],
                                                                    'tax': data['tax'] })
        
        return render(request, "invoice_generator/form.html")


    
class SearchView(TemplateView):

    template_name = "invoice_generator/search.html"
    form_class = SearchForm

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            data = invoice_search(form.data)

            if data is not False:
                return render(request, "invoice_generator/search.html", {"invoices_found": data['invoices_found'] })

            return render(request, "invoice_generator/search.html")



            
