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



"""

    Logic

"""

# Edits Product and handles the POST data from products/edit_product form
def product_edit(request):


    return redirect('/dashboard/products')


# Delete product selected in products.html, the redirects back to products page
def delete_product(request, id):

    return redirect('/dashboard/products')
