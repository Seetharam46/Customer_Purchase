from django.shortcuts import render
import pandas as pd
from django.core.files.storage import FileSystemStorage

def index(request):
    result = ""
    if request.method == "POST" and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        # Save the uploaded file to a temporary location
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.url(filename)

        # Read the uploaded Excel file
        df = pd.read_excel(f".{file_path}").fillna("")  # Read the file dynamically

        search_type = request.POST.get('search_type')
        search_value = request.POST.get('search_value')

        if search_type == "name":
            result = get_customer_data(df, search_value)
        elif search_type == "product":
            result = get_customers_by_product(df, search_value)

    return render(request, 'index.html', {'result': result})

def get_customer_data(df, name):
    name_lower = name.lower()
    df['Customer Name Lower'] = df['Customer Name'].str.lower()
    result = df[df['Customer Name Lower'] == name_lower].drop(columns=["Customer Name", "Customer Name Lower"]).values.flatten()
    products = [product for product in result if product != ""]
    if not products:
        return f"No products found for {name}."
    return f"{name}: {', '.join(products)}"

def get_customers_by_product(df, product_name):
    product_name_lower = product_name.lower()
    matching_rows = df.apply(lambda row: product_name_lower in [str(p).lower() for p in row[1:4]], axis=1)
    customers = df[matching_rows]["Customer Name"].values
    if not customers.size:
        return f"No customers found who bought {product_name}."
    return f"Customers who bought {product_name}: {', '.join(customers)}"
