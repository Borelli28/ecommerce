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
            errors["email"] = "Email already exist. Please enter a different email or Login In."

        return errors

    def login_validator(self, postData):
        errors = {}

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        #DOES NOT WORK I INPUT THE RIGHT PASSWORD AND IT STILL TELLS ME: WRONG PASSWORD
        # returns error message if passowrd does not exist in database
        # if Seller.objects.filter(password=postData['password']):
        #     pass
        # else:
        #     errors['password'] = "Wrong Password"

        if len(postData['email']) < 3:
            errors['email'] = "Please enter am Email longer than 3 characters"

        # returns error message if the email does not exist in database
        if Seller.objects.filter(email=postData['email']):
            pass
        else:
            errors['email'] = "Wrong Email"

        return errors

class Customer(models.Model):

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    ship_addr = models.CharField(max_length=255)
    bill_addr = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    img = models.FileField(upload_to='static/images/products', default="no-product-image.png")
    category = models.ForeignKey(Category, related_name="category", on_delete=models.CASCADE)
    desc = models.CharField(max_length=255)
    sold_by = models.ForeignKey(Seller, related_name="seller", on_delete=models.CASCADE)
    # Pur_cuont = Quantity Sold
    pur_count = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):

    submitted_by = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE)
    #product ids in a string, but separated by a coma: "1,5,2,13"
    product_id = models.IntegerField()
    total = models.DecimalField(max_digits=19, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
