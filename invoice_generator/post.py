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
    invoice_num = int(data['invoice_num'])
    company_id = int(data['company_id'])
    if "add_product" in data: 
        products = {"name": data['product_name'], 
                          "quantity": int(data['quantity']), 
                          "measure": data['measure'], 
                          "unit_price": float(data['unit_price']), 
                          "value": float(data['value'])}
    elif "delete_product" in data:
        try:
            del_index = int(request.POST['delete_product'][-1])
            invoice = Invoice.objects.filter(invoice_num=invoice_num)
            serializer = InvoiceSerializer(invoice)
            del serializer.data['products'][del_index]
            if serializer.is_valid():
                serializer.save()
        except:
            pass
    try:
        invoice = Invoice.objects.get(invoice_num=invoice_num)
        serializer = InvoiceSerializer(invoice)
        serializer.data['products'].append(products)
        invoice_data = serializer.data
    except:  
        invoice_data = {
                "invoice_num": invoice_num,
            	"date": data['date'],
            	"company_id": company_id,
            	"place": data['place'],
            	"products": [],
                "tax": {
            		"tax_base": 0.0,
            		"tax_rate": 0.0,
            		"payment_amount": 0.0
            	}
            }
        invoice_data['products'].append(products)
        
    serializer = InvoiceSerializer(data = invoice_data)
    if serializer.is_valid():
        serializer.save()
    products = serializer.data['products']
    company_data = check_company_id(request)
    company_data[3] = request.POST['company_manager']
    return { 'products': products, 
            'invoice_num': invoice_num, 
            'date': data['date'],
            'company_id': company_id,
            'company_data': company_data,
            'place': data['place'] }