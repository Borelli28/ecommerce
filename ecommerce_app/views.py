from django.shortcuts import render, redirect
from ecommerce_app.models import *
from django.contrib import messages
import bcrypt

# python manage.py

# renders login page
def login(request):

    return render(request, 'login.html')

# Renders dashboard html Page. Also gives the data used to personalized the dashboard page
def dashboard(request):

    all_products = Product.objects.all()
    # mvps_products = []
    #current login seller
    log_seller_id = request.session['sellerid']
    log_seller = Seller.objects.get(id=log_seller_id)
    # Gets the most purchased product of the current seller, if the the seller has products posted in the DB.
    if Product.objects.filter(sold_by=log_seller):
        all_pur_counts = []
        for product in all_products:
            # if the product was posted by the login seller
            if product.sold_by == Seller.objects.get(id=log_seller_id):
                all_pur_counts.append(product.pur_count)
        print(all_pur_counts)
        # MAX() method get the greatest value in an array of integers
        # so mvp has the greatest number in all the product purchases counts
        mvp = max(all_pur_counts)
        print(mvp)
        # gets the instance of the most purchased product using the mvp integer
        mvp_instance = all_products.filter(pur_count=mvp)
        print(mvp_instance)

    # now lets get the mvp product in between all sellers combined, if there is products in the database
    if len(all_products) > 0:
        # if there is at least three products in the database. Else just return the same element three times
        if len(all_products) >=3:
            all_pur_counts = []
            for product in all_products:
                all_pur_counts.append(product.pur_count)
            print(all_pur_counts)
            # MAX() method get the greatest value in an array of integers
            # get the max value then pop it out of the array until we get the 3 largest values in the array
            mvp = max(all_pur_counts)
            print(mvp)
            second_mvp = max(all_pur_counts)
            third_mvp = max(all_pur_counts)
            # gets the instance of the most purchased product using the mvp integer
        # Else just return the same element three times
        else:
            all_pur_counts = []
            for product in all_products:
                all_pur_counts.append(product.pur_count)
            print(all_pur_counts)
            # MAX() method get the greatest value in an array of integers
            # get the max value then pop it out of the array until we get the 3 largest values in the array
            mvp = max(all_pur_counts)
            mvp_one = all_products.filter(pur_count=mvp)
            mvp_two = all_products.filter(pur_count=mvp)
            mvp_three = all_products.filter(pur_count=mvp)
            print(mvp_one)
            print(mvp_two)
            print(mvp_three)



    # Pass: last product added, most purchased product & most purschased product from all sellers data.
    context = {"last_product":Product.objects.last(), "most_pur_product_seller":mvp_instance, "mvp_one": mvp_one, "mvp_two": mvp_two, "mvp_three": mvp_three}


    return render(request, 'dashboard.html', context)

# Renders the orders page and shows orders info
def orders(request):

    # need to give the orders of the current seller, also the instance of the customer that make the order
    all_orders = Order.objects.all()

    for order in all_orders:
        # for each order it will grab that order product id
        order_product = Product.objects.get(id=order.product_id)

        our_seller = Seller.objects.get(id=request.session['sellerid'])
        seller_orders = []
        # if the current product is sold by our seller and the current order is not already in our seller orders list
        # then add order to seller_orders
        if order_product.sold_by.email == our_seller.email and order not in seller_orders:
            seller_orders.append(order)
            print("Order added to seller orders")
            print(order)
    print("All seller orders:")
    print(seller_orders)

    context = {"orders": seller_orders}

    return render(request, 'orders.html', context)

# Render the display order Page
def order_show(request, id):

    # Using product id, get order, customer & and product
    order = Order.objects.get(id=id)
    customer = order.submitted_by
    product_id = order.product_id
    product = Product.objects.get(id=product_id)
    #calculate total of order: order.total + $3 Shipping
    total = order.total + 3

    context = {"order": order, "customer":customer, "product":product, "order_total":total}

    return render(request, 'order_show.html', context)

# Renders the products html
def products(request):

    all_products = Product.objects.all()
    our_seller = Seller.objects.get(id=request.session['sellerid'])
    seller_products = []
    # get the products of our seller
    for product in all_products:
        if product.sold_by.email == our_seller.email:
            seller_products.append(product)
    print(seller_products)
    context = {"products":seller_products}

    return render(request, 'products.html', context)

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

# Handles data from registration form in login Page
def register_seller(request):

    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Seller.objects.seller_register_val(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the blog to be updated, make the changes, and save

        _first_name = request.POST['first_name']
        _last_name = request.POST['last_name']
        _email = request.POST['email']
        _password = request.POST['password']

        # Hash the password using bcrypt
        pw_hash = bcrypt.hashpw(_password.encode(), bcrypt.gensalt()).decode()
        # Create the object instance
        Seller.objects.create(first_name=_first_name, last_name=_last_name, email=_email, password=pw_hash)

        print("POST data:")
        print(_first_name)
        print(_last_name)
        print(_email)
        print(pw_hash)

        print("Seller Created:")
        print(Seller.objects.last())

        return redirect('/')

# handles the data from seller login form in login.html
def log_seller(request):

    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Seller.objects.login_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    else:
        # see if the username provided exists in the database. Seller uses filter because it will return a list of sellers that have the provided email
        seller = Seller.objects.filter(email=request.POST['email'])
        print("Inside log_user method")

        if len(seller) > 0: # note that we take advantage of truthiness here: an empty list will return false
            logged_seller = seller[0]
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            print("inside the first if statement")
            if bcrypt.checkpw(request.POST['password'].encode(), logged_seller.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['sellerid'] = logged_seller.id

                # saves email in session so we can use it to check if user is log-in in success.
                request.session['email'] = request.POST['email']

                # never render on a post, always redirect!
                return redirect('/dashboard')

    # if we didn't find anything in the database by searching by username or if the passwords don't match,
    # redirect back to a safe route
    return redirect('/')

# Edits Product and handles the POST data from products/edit_product form
def product_edit(request):

    return redirect('/dashboard/products')

# Delete product selected in products.html, the redirects back to products page
def delete_product(request, id):

    return redirect('/dashboard/products')

# Creates a new Product using the POST data from add a new product page form, and then redirects to products Page
def create_product(request):

    return redirect('/dashboard/products')

# Clear all data in session
def clear(request):

    request.session.clear()
    print("Session cleared")

    return redirect('/')
