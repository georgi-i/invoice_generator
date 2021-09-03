from requests import get
from re import search, DOTALL

from .models import Invoice
from .serializers import InvoiceSerializer


def check_company_id(request):
            
    company_data = []
    try:
        company_id = request.POST['company_id']
        cookies = {'CONSENT': 'YES+1'}
        r_google = get(f'https://www.google.com/search?q={company_id}+papagal', cookies=cookies)
        m_url = search(r'https:\/\/papagal\.bg\/eik\/\d+\/[\da-zA-Z]{4}', r_google.text)
        r_papagal = get(m_url.group(0), cookies=cookies)
        m_company_data = search(r'@context.+\"address\":.+гр\.\s(.+?),\s(.+?)\",\".+\"legalName\":\s\"(.+)\"}', r_papagal.text, flags=DOTALL)
        m_company_manager = search(r'\"founder\":\s\"(.+?)\"', r_papagal.text, flags=DOTALL)
        if m_company_manager is None:
            m_company_manager = ''
        else:
            m_company_manager = m_company_manager.group(1)
        company_data = [m_company_data.group(3), m_company_data.group(1), m_company_data.group(2), m_company_manager]
    except:
        return None

    return { 'company_data': company_data, 
             'company_id': company_id,
             'invoice_num': request.POST['invoice_num'], 
             'date': request.POST['date'],
             'place': request.POST['place'] }


def handle_request(request, data):
    
    products = {}
    try:
        tax_value = float(data['value'])
    except:
        tax_value = 0.0   
    invoice_num = int(data['invoice_num'])
    company_id = int(data['company_id'])
    if "add_product" in data: 
        products = {"name": data['product_name'], 
                          "quantity": int(data['quantity']), 
                          "measure": data['measure'], 
                          "unit_price": float(data['unit_price']), 
                          "value": tax_value }
    elif "delete_product" in data:
        try:
            del_index = int(request.POST['delete_product'][-1]) - 1
            invoice = Invoice.objects.get(invoice_num=invoice_num)
            serializer = InvoiceSerializer(invoice)
            serializer.data['tax']['tax_base'] -= tax_value
            serializer.data['tax']['tax_rate'] -= tax_value * 0.2
            serializer.data['tax']['payment_amount'] -= tax_value * 1.2
            del serializer.data['products'][del_index]
            serializer.update(invoice, serializer.data)
            
            company_data = [ data['company_name'], 
                     data['company_city'], 
                     data['company_address'], 
                     data['company_manager'] ]

            tax = [ f'{serializer.data["tax"]["tax_base"]:.2f}', 
                    f'{serializer.data["tax"]["tax_rate"]:.2f}', 
                    f'{serializer.data["tax"]["payment_amount"]:.2f}' ]

            return { 'products': serializer.data['products'],
                    'invoice_num': invoice_num, 
                    'date': data['date'],
                    'company_id': company_id,
                    'company_data': company_data,
                    'place': data['place'],
                    'tax': tax } 
        except:
            pass
    
    try:
        invoice = Invoice.objects.get(invoice_num=invoice_num)
        serializer = InvoiceSerializer(invoice)
        serializer.data['products'].append(products)
        serializer.data['tax']['tax_base'] += tax_value
        serializer.data['tax']['tax_rate'] += tax_value * 0.2
        serializer.data['tax']['payment_amount'] += tax_value * 1.2
        serializer.update(invoice, serializer.data)
    except:  
        invoice_data = {
                "invoice_num": invoice_num,
            	"date": data['date'],
            	"company_id": company_id,
                "company_name": data['company_name'],
                "company_city": data['company_city'],
                "company_address": data['company_address'],
                "company_manager": data['company_manager'],
            	"place": data['place'],
            	"products": [],
                "tax": {
            		"tax_base": tax_value,
            		"tax_rate": tax_value * 0.2,
            		"payment_amount": tax_value * 1.2
            	}
            }
        invoice_data['products'].append(products) 
        serializer = InvoiceSerializer(data = invoice_data)
        if serializer.is_valid():
            serializer.save()

    products = serializer.data['products']
    company_data = [ data['company_name'], 
                     data['company_city'], 
                     data['company_address'], 
                     data['company_manager'] ]

    tax = [ f'{serializer.data["tax"]["tax_base"]:.2f}', 
            f'{serializer.data["tax"]["tax_rate"]:.2f}', 
            f'{serializer.data["tax"]["payment_amount"]:.2f}' ]

    return { 'products': products, 
            'invoice_num': invoice_num, 
            'date': data['date'],
            'company_id': company_id,
            'company_data': company_data,
            'place': data['place'], 
            'tax': tax }