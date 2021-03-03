from django.db import models

class Customer(models.Model):

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    shipp_addr = models.CharField(max_length=255)
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

class Category(models.Model):

    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    inv_count = models.IntegerField()
    img = FileField(upload_to='products_images/', null=True)
    category = models.ForeignKey(Category, related_name="category", on_delete=models.CASCADE)
    desc = models.CharField(max_length=255)
    sold_by = models.ForeignKey(Seller, related_name="seller", on_delete=models.CASCADE)
    pur_count = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):

    customer = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):

    customer = models.ForeignKey(Cart, related_name="customer", on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, related_name="seller", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
