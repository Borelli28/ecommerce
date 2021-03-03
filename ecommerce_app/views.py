from django.shortcuts import render, redirect
from ecommerce_app.models import *
from django.contrib import messages
import bcrypt

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

        return redirect('/dashboard')

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
                request.session['userid'] = logged_seller.id

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
