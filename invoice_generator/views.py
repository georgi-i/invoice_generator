from rest_framework import viewsets
from django.views.generic import TemplateView
from .forms import InvoiceForm
from django.shortcuts import render
from .post import check_company_id, handle_request


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
                                                                    'place': data['place']})
        return render(request, "invoice_generator/form.html")


    
class SearchView(TemplateView):

    template_name = "invoice_generator/search.html"



            
