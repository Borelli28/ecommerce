from django.db import models

# python manage.py

class ValidatorManager(models.Manager):

    def seller_register_val(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Passwords do not match"

        # Check if email already exist in database
        if Seller.objects.filter(email=postData['email']):
            errors["email"] = "Email already exist. Please enter a different email or Log-In into your account."

        return errors

    def customer_register_val(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Passwords do not match"

        # Check if email already exist in database
        if Customer.objects.filter(email=postData['email']):
            errors["email"] = "Email already exist. Please enter a different email or Log-In into your account."

        return errors

    def seller_login_validator(self, postData):
        errors = {}

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if len(postData['email']) < 3:
            errors['email'] = "Please enter am Email longer than 3 characters"

        # returns error message if the email does not exist in database
        if Seller.objects.filter(email=postData['email']):
            pass
        else:
            errors['email'] = "Wrong Email"

        return errors

    def customer_login_validator(self, postData):
        errors = {}

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"


        if len(postData['email']) < 3:
            errors['email'] = "Please enter am Email longer than 3 characters"

        # returns error message if the email does not exist in database
        if Customer.objects.filter(email=postData['email']):
            pass
        else:
            errors['email'] = "Wrong Email"

        return errors

    def add_product_validator(self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors["name"] = "Product Name should be at least 2 characters long"

        if len(postData['price']) < 1:
            errors["price"] = "Please input a valid price for the product"

        if len(postData['inv_count']) < 1:
            errors["inv_count"] = "Please enter a valid input for Inventory Count"

        if len(postData['description']) < 1:
            errors["description"] = "Please enter a description for the product"

        if len(postData['cat_sel']) < 1 and len(postData['add_cat']) < 1:
            errors["cat_sel"] = "Please either select one Category from the dropdown menu or create a new category"

        return errors

    def payment_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters long"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters long"

        if len(postData['addr']) < 7:
            errors['addr'] = "Address should be at least 7 characters. Make sure to include Zip Code, State & Street Address."

        # Billing inputs validators
        if len(postData['first_name_bill']) < 2:
            errors['first_name_bill'] = "First Name should be at least 2 characters long"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters long"

        if len(postData['addr_bill']) < 7:
            errors['addr_bill'] = "Address should be at least 7 characters. Make sure to include Zip Code, State & Street Address."

        if len(postData['card_number']) != 16:
            errors['card_number'] = "Card number does not seems correct. Card number should be a 16 digits number with no spaces"

        if len(postData['sec_code']) != 3:
            errors['sec_code'] = "Security code does not seems correct. Security Code should be at an 3 digits code with no spaces in between"

        if len(postData['exp_date']) > 8:
            errors['exp_date'] = "Make sure to pick the month and year of expiration date"

        return errors

class Customer(models.Model):

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidatorManager()

class Seller(models.Model):

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidatorManager()

class Category(models.Model):

    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    inv_count = models.IntegerField()
    img = models.ImageField(upload_to='products_img/', blank=True, default="no-product-image.png")
    category = models.ForeignKey(Category, related_name="category", on_delete=models.CASCADE)
    desc = models.CharField(max_length=255)
    sold_by = models.ForeignKey(Seller, related_name="seller", on_delete=models.CASCADE)
    # Pur_count = Quantity Sold
    pur_count = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidatorManager()

class Order(models.Model):

    submitted_by = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE)
    #product ids in a string, but separated by a coma: "1,5,2,13"
    product_id = models.IntegerField()
    total = models.DecimalField(max_digits=19, decimal_places=2)
    ship_addr = models.CharField(max_length=255)
    # in-process, shipped or cancelled
    status = models.CharField(max_length=10 ,default="in-process")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidatorManager()
