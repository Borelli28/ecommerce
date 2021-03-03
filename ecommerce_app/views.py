from django.shortcuts import render, redirect

# python manage.py

# renders login page
def login(request):

    return render(request, 'login.html')

# Renders dashbaord html Page
def dashboard(request):

    return render(request, 'dashboard.html')

# Renders the orders page
def orders(request):

    return render(request, 'orders.html')

# Render the display order Page
def order_show(request, id):

    context = {"id": id}

    return render(request, 'order_show.html', context)

# Renders the products html
def products(request):

    return render(request, 'products.html')

# Renders the products/ edit_product page
def edit_product(request, id):

    context = {"id": id}

    return render(request, 'edit_product.html', context)

# Renders add new product Page
def add_product(reques):

    return render(reques, 'add_product.html')


"""

    LOGIC

"""

# Edits Product and handles the POST data from products/edit_product form
def product_edit(request):


    return redirect('/dashboard/products')


# Delete product selected in products.html, the redirects back to products page
def delete_product(request, id):

    return redirect('/dashboard/products')

# Creates a new Product using the POST data from add a new product page form, and then redirects to products Page
def create_product(request):


    return redirect('/dashboard/products')
