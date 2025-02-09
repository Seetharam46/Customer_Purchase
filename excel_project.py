import pandas as pd

file_path = r"D:\Projects\Customer_Purchase_Project\customers_purchases.xlsx"
df = pd.read_excel(file_path).fillna("")
df.columns = df.columns.str.lower()

def get_customer_data(name):
    name_lower = name.lower()
    if "customer name" not in df.columns:
        return "Error: 'Customer Name' column not found."
    
    result = df[df["customer name"].str.lower() == name_lower].drop(columns=["customer name"]).values.flatten()
    products = [product for product in result if product != ""]
    
    return f"{name}: {', '.join(products)}" if products else f"No products found for {name}."

def get_customers_by_product(product_name):
    product_lower = product_name.lower()
    if "customer name" not in df.columns:
        return "Error: 'Customer Name' column not found."
    
    matching_rows = df.apply(lambda row: product_lower in [str(p).lower() for p in row[1:4]], axis=1)
    customers = df[matching_rows]["customer name"].values
    
    return f"Customers who bought {product_name}: {', '.join(customers)}" if customers.size else f"No customers found who bought {product_name}."

search_type = input("Choose: Search by (name/product): ").strip().lower()
search_value = input("Enter search value: ").strip()

if search_type == "name":
    print(get_customer_data(search_value))
elif search_type == "product":
    print(get_customers_by_product(search_value))
else:
    print("Invalid search type. Please enter 'name' or 'product'.")
