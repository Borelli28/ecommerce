from django.shortcuts import render, redirect
from ecommerce_app.models import *
from django.contrib import messages
import bcrypt

# python manage.py

# renders login page
def login(request):

    return render(request, 'seller_templates/login.html')

# Renders dashboard html Page. Also gives the data used to personalized the dashboard page
def dashboard(request):

    all_products = Product.objects.all()

    # mvps_products = []
    #current login seller
    log_seller_id = request.session['sellerid']
    log_seller = Seller.objects.get(id=log_seller_id)
    mvp_instance = ""
    # Gets the most purchased product of the current seller, if the the seller has products posted in the DB.
    if Product.objects.filter(sold_by=log_seller):
        all_pur_counts = []
        for product in all_products:
            all_products_seller = []
            # if the product was posted by the login seller
            if product.sold_by == Seller.objects.get(id=log_seller_id):
                all_products_seller.append(product)
                all_pur_counts.append(product.pur_count)

                # get the last product added from the seller:
                seller_last_prod = all_products_seller[-1]

            if product.sold_by == Seller.objects.get(id=log_seller_id):
                print(all_pur_counts)
                # MAX() method get the greatest value in an array of integers
                # so mvp has the greatest number in all the product purchases counts
                mvp = max(all_pur_counts)
                print(mvp)
                # gets the instance of the most purchased product using the mvp integer
                mvp_instance_raw = all_products.filter(pur_count=mvp)
                # check the mvp_instance_raw is a product sold_by seller
                for i in mvp_instance_raw:
                    if i.sold_by:
                        mvp_instance = i
                        # print("MVP Instance:")
                        # print(mvp_instance)

    # now lets get the mvp product in between all sellers combined, if there is products in the database
    if len(all_products) > 0:
        # if there is at least three products in the database. Else just return the same element three times
        if len(all_products) >=3:
            all_pur_counts = []
            for product in all_products:
                all_pur_counts.append(product.pur_count)
            # print(all_pur_counts)
            # MAX() method get the greatest value in an array of integers
            # get the max value then pop it out of the array until we get the 3 largest values in the array
            mvp_one = max(all_pur_counts)
            all_pur_counts.remove(mvp_one)
            mvp_two = max(all_pur_counts)
            all_pur_counts.remove(mvp_two)
            mvp_three = max(all_pur_counts)
            # gets the instance of the most purchased product using the mvp integer
        # Else just return the same element three times
        else:
            all_pur_counts = []
            for product in all_products:
                all_pur_counts.append(product.pur_count)
            # print(all_pur_counts)
            # MAX() method get the greatest value in an array of integers
            # get the max value then pop it out of the array until we get the 3 largest values in the array
            mvp = max(all_pur_counts)
            mvp_one = all_products.filter(pur_count=mvp)
            mvp_two = all_products.filter(pur_count=mvp)
            mvp_three = all_products.filter(pur_count=mvp)
    print("MVP One:")
    print(mvp_one)
    print("MVP Two:")
    print(mvp_two)
    print("MVP Three:")
    print(mvp_three)

    # Pass: last product added, most purchased product & most purschased product from all sellers data.
    context = {"last_product":seller_last_prod, "most_pur_product_seller":mvp_instance, "mvp_one": mvp_one, "mvp_two": mvp_two, "mvp_three": mvp_three}


    return render(request, 'seller_templates/dashboard.html', context)

# Renders the orders page and shows orders info
def orders(request):

    # need to give the orders of the current seller, also the instance of the customer that make the order
    all_orders = Order.objects.all()
    seller_orders = []
    for order in all_orders:
        # for each order it will grab that order product
        order_product = Product.objects.get(id=order.product_id)

        our_seller = Seller.objects.get(id=request.session['sellerid'])
        # if the current product is sold by our seller
        # then add order to seller_orders
        if order_product.sold_by.email == our_seller.email:
            print("Seller Email:")
            print(our_seller.email)
            print("Sold by Email:")
            print(order_product.sold_by.email)
            # if the product has an order then add that product to seller_orders
            if (order_product in seller_orders) == False:
                seller_orders.append(order)
    print("All seller orders:")
    print(seller_orders)

    context = {"orders": seller_orders}

    return render(request, 'seller_templates/orders.html', context)

# Render the display order Page
def order_show(request, id):

    # Using product id, get order, customer & and product
    order = Order.objects.get(id=id)
    customer = order.submitted_by
    product_id = order.product_id
    product = Product.objects.get(id=product_id)
    # calculate order Shipping and gives the total cost of the transaction
    ship_price = float(0.025)
    ship_cost = float(order.total) * ship_price
    total = float(order.total) + ship_cost

    # this color is used in the page in the status of the order
    color = "white"
    if order.status == "in-process":
        color = "grey"
    elif order.status == "shipped":
        color = "green"
    elif order.status == "cancelled":
        color = "red"

    context = {"order": order, "customer":customer, "product":product, "order_total":total, "color": color}

    return render(request, 'seller_templates/order_show.html', context)

# Renders the products html
def products(request):

    all_products = Product.objects.all()
    our_seller = Seller.objects.get(id=request.session['sellerid'])
    seller_products = []
    # get the products of our seller
    for product in all_products:
        if product.sold_by.email == our_seller.email:
            seller_products.append(product)

    context = {"products":seller_products}


    return render(request, 'seller_templates/products.html', context)

# Renders the products/ edit_product page
def edit_product(request, id):

    # get product instance
    product = Product.objects.get(id=id)

    # get Categories
    cats = Category.objects.all()

    context = {"product": product, "cats": cats}

    return render(request, 'seller_templates/edit_product.html', context)

# Renders add new product Page
def add_product(request):

    context = {"categories":Category.objects.all()}

    return render(request, 'seller_templates/add_product.html', context)

"""

    LOGIC - SELLER SITE

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

        _first_name = request.POST['first_name']
        _last_name = request.POST['last_name']
        _email = request.POST['email']
        _password = request.POST['password']

        # Hash the password using bcrypt
        pw_hash = bcrypt.hashpw(_password.encode(), bcrypt.gensalt()).decode()
        # Create the object instance
        seller = Seller.objects.create(first_name=_first_name, last_name=_last_name, email=_email, password=pw_hash)

        print("POST data:")
        print(_first_name)
        print(_last_name)
        print(_email)
        print(pw_hash)

        print("Seller Created:")
        print(Seller.objects.last())

        # save the sellerid in session
        request.session['sellerid'] = seller.id

        return redirect('/dashboard')

# handles the data from seller login form in login.html
def log_seller(request):

    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Seller.objects.seller_login_validator(request.POST)
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
def product_edit(request, id):

    # get the instance using the id
    product = Product.objects.get(id=id)

    # current log-in seller:
    seller = Seller.objects.get(id=request.session['sellerid'])


    # grabs all post data and edits the field if a value is given in POST
    if len(request.POST['name']) > 0:
        post_name = request.POST['name']
        product.name = post_name
        product.save()

    if len(request.POST['price']) > 0:
        post_price = request.POST['price']
        product.price = post_price
        product.save()
    if len(request.POST['inv_count']) > 0:
        post_inv_count = request.POST['inv_count']
        product.inv_count = post_inv_count
        product.save()
    if len(request.POST['description']) > 0:
        post_desc = request.POST['description']
        product.desc = post_desc
        product.save()
    # if the dropdown menu is empty, that means user wants to create new category
    # because he did not select any categories from dropdown-menu
    if request.POST['cat_sel'] == "blank" and len(request.POST['add-cat']) > 0:
        print("cat_sel is blank")
        # Checks if the user input something into add_cat Form
        # If he didn't then redirect back to page
        if len(request.POST['add-cat']) > 0:
            cat_post = request.POST['add-cat']
            # create category instance:
            new_cat = Category.objects.create(name=cat_post)
            _cat = new_cat
            print("Category Created:")
            print(_cat)
            product.category = _cat
            product.save()
        else:
            print("User need to either create a new category or select one from the dropdown menu")
            return redirect('/add_product')
    elif request.POST['cat_sel'] != "blank":
        cat_id = request.POST['cat_sel']
        _cat = Category.objects.get(id=int(cat_id))
        product.category = _cat
        product.save()

    if len(request.FILES['upload-img']) > 0:
        image = request.FILES['upload-img']
        product.img = image
        product.save()
        print(image)

    print("Product has being edited:")
    print(product)

    return redirect('/dashboard/products')

# Delete product selected in products.html, the redirects back to products page
def delete_product(request, id):

    # get the product instance using the id
    product = Product.objects.get(id=id)

    product.delete()

    return redirect('/dashboard/products')

# Creates a new Product using the POST data from add a new product page form, and then redirects to products Page
def create_product(request):

        # pass the post data to the method we wrote and save the response in a variable called errors
        errors = Product.objects.add_product_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/add_product')

        else:
            # current log-in seller:
            seller = Seller.objects.get(id=request.session['sellerid'])


            # grabs all post data
            name = request.POST['name']
            price = request.POST['price']
            inv_count = request.POST['inv_count']
            desc = request.POST['description']
            #if the dropdown menu is empty, that means user wants to create new category
            if request.POST['cat_sel'] == "blank":
                print("cat_sel is blank")
                # Checks if the user input something into add_cat Form
                # If he didn't then redirect back to page
                if len(request.POST['add-cat']) > 0:
                    cat_post = request.POST['add-cat']
                    # create category instance:
                    new_cat = Category.objects.create(name=cat_post)
                    _cat = new_cat
                    print("Category Created:")
                    print(_cat)
                else:
                    print("User need to either create a new category or select one from the dropdown menu")
                    return redirect('/add_product')
            else:
                cat_id = request.POST['cat_sel']
                _cat = Category.objects.get(id=int(cat_id))

            image = request.FILES['upload-img']

            print(name)
            print(price)
            print(inv_count)
            print(desc)
            print(_cat)
            print(image)

            # create product instance:
            new_product = Product.objects.create(name=name, price=price, inv_count=inv_count, img=image, category=_cat, desc=desc, sold_by=seller, pur_count=0)

            return redirect('/dashboard/products')

# Handles the post data from orders.html select status Form
def update_status_order(request, id):

    # gets the instance of the order using the id
    order = Order.objects.get(id=id)

    # if post data is not empty, update the order.status with the post status
    if len(request.POST['order_status']) > 0:
        post_status = request.POST['order_status']
        order.status = post_status
        order.save()
        print("Order status updated to:")
        print(post_status)

    return redirect('/dashboard/orders')

# Clear all data in session
def clear(request):

    request.session.clear()
    print("Session cleared")

    return redirect('/')



'''


Customer site methods


'''

# renders customer login page
def login_page(request):

    # clear all data in session
    request.session.clear()
    print("All data stored in session has been erased")

    return render(request, 'customer_templates/login.html')

# renders the customer site home Page
def home(request):
    # if customer is logged in already then gives access to the home page
    if 'customerid' in request.session:

        #if cart is empty then display 0 in quantity in cart
        if 'quantity_of_products' not in request.session:
            request.session['quantity_of_products'] = 0

        all_products = Product.objects.all()
        all_cats = Category.objects.all()

        context = {"products":all_products, "cats":all_cats}

        return render(request, 'customer_templates/home.html', context)

    # else if not currently logged in then redirect to the customer login page
    else:
        return redirect('/login')

# renders the home page but only showing the products under the customer selected category
def home_category(request, id):
    # if customer is logged in already then gives access to the home page
    if 'customerid' in request.session:
        # gets the category instance using the id
        category_sel = Category.objects.get(id=id)
        # get all products in category selected

        all_products = Product.objects.all()
        all_cats = Category.objects.all()

        context = {"products":all_products, "cats":all_cats, "category":category_sel}

        return render(request, 'customer_templates/home_cat.html', context)

    else:
        return redirect('/login')

# renders the show selected product page
def show(request, id):

    # if customer is logged in already then gives access to the home page
    if 'customerid' in request.session:
        # get the product using id
        product = Product.objects.get(id=id)
        print("Product selected by user:")
        print(product.name)

        # Get the items in the same categories that the current product being displayed
        #get the category of the current product
        current_cat = product.category
        print("Current Product Category")
        print(current_cat)
        # get all products with the same category for use in: similar items
        similar_items = Product.objects.filter(category=current_cat)
        print("Similar Items:")
        print(similar_items)

        context = {"product": product, "similar_items": similar_items}

        return render(request, 'customer_templates/product_show.html', context)
    else:
        return redirect('/login')

# renders page to process user orders and payment
def show_cart(request):
    # if customer is logged in already then gives access to the home page
    if 'customerid' in request.session:

        # only show the page if there is products in cart
        if 'product_in_cart' in request.session:

            product_id = request.session['product_in_cart']
            product = Product.objects.get(id=product_id)
            quantity = request.session['quantity_of_products']
            print("Product in cart")
            print(product.name)
            print("This quantity selected:")
            print(quantity)

            context = {"product":product, "quantity":quantity}

            return render(request, 'customer_templates/cart_show.html', context)

        else:
            return redirect('/home')
    else:
        return redirect('/login')

"""

    LOGIC - CUSTOMER SITE

"""

def register_customer(request):

    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Customer.objects.customer_register_val(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/login')

    else:
        # if the errors object is empty, that means there were no errors!

        _first_name = request.POST['first_name']
        _last_name = request.POST['last_name']
        _email = request.POST['email']
        _password = request.POST['password']

        # Hash the password using bcrypt
        pw_hash = bcrypt.hashpw(_password.encode(), bcrypt.gensalt()).decode()
        # Create the object instance
        customer = Customer.objects.create(first_name=_first_name, last_name=_last_name, email=_email, password=pw_hash)

        print("POST data:")
        print(_first_name)
        print(_last_name)
        print(_email)
        print(pw_hash)

        print("Customer registered")
        print(Customer.objects.last())

        # save the sellerid in session
        request.session['customerid'] = customer.id

        return redirect('/home')

# Handles the data from customer login form and if user exist in db,
# save the id of user in session and redirect to home page
def log_customer(request):

    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Customer.objects.customer_login_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/login')

    else:
        # see if the username provided exists in the database. Seller uses filter because it will return a list of sellers that have the provided email
        customer = Customer.objects.filter(email=request.POST['email'])
        print("Inside log_customer method")

        if len(customer) > 0:
            logged_customer = customer[0]
            # assuming we only have one customer with this username, the customer would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password'].encode(), logged_customer.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['customerid'] = logged_customer.id

                # never render on a post, always redirect!
                return redirect('/home')

    # if we didn't find anything in the database by searching by username or if the passwords don't match,
    # redirect back to a safe route
    return redirect('/login')

# Handles product to be added to cart data and then redirect back to home but
# displays an alert to the user that items were added to cart
def cart(request, id):

    # get the quanity of the product to add to cart(1, 2 or 3) from select from
    quantity = request.POST['num_products']
    print("Quanity to be added to Cart:")
    print(quantity)

    # saves in session the quantity and the products currently in the customer cart
    request.session['product_in_cart'] = id
    request.session['quantity_of_products'] = quantity

    print("Add this product to cart:")
    print(id)
    print("This quantity selected:")
    print(quantity)

    return redirect('/home')

# Process the customer payment then clear the sessions and redirect to home
# with an alert saying that the order was placed sucessfully
def payment(request, prod_id):

    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Order.objects.payment_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/cart_show')

    else:
        # if the errors object is empty, that means there were no errors!

        _first_name = request.POST['first_name']
        _last_name = request.POST['last_name']
        _addr = request.POST['addr']
        _total = request.POST['total']

        print("POST data:")
        print(_first_name)
        print(_last_name)
        print(_addr)


        # gets customer instance using the id of the current logged in customer
        logged_customer = Customer.objects.get(id=request.session['customerid'])

        # create order instance
        new_order = Order.objects.create(submitted_by=logged_customer, product_id=prod_id, total=_total, ship_addr=_addr)

        # Update the inventory count and the Purchased counter of the product bought
        quantity_purchased = request.session['quantity_of_products']
        # get the product instance
        product = Product.objects.get(id=prod_id)

        product_inv_count = product.inv_count
        product_pur_count = product.pur_count
        print("Old inv_count:")
        print(product_inv_count)
        print("Old pur_count:")
        print(product_pur_count)

        new_inv = product_inv_count - int(quantity_purchased)
        new_pur = product_pur_count + int(quantity_purchased)
        product.inv_count = new_inv
        product.pur_count = new_pur
        product.save()

        print("new inv_count:")
        print(product.inv_count)
        print("new pur_count:")
        print(product.pur_count)

        print("Order Created:")
        print(Order.objects.last())

        return redirect('/clear_cart')

# Clear cart session data
def clear_cart(request):

    request.session['quantity_of_products'] = 0
    del request.session['product_in_cart']
    print("Cart cleared")

    return redirect('/home')
