from django.contrib.auth.models import User
from django.db import models 

class Vendor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    store_name=models.CharField(max_length=255)
    whatsapp_number=models.CharField(max_length=15) 
    
    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name=models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    postman = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postman_products')  # Postman who posted the product
    name=models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    image=models.ImageField(upload_to='media/product_images')
    is_trending = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_reviews')
    content = models.TextField()
    rating = models.IntegerField(default=1)  # Rating from 1 to 5

    def __str__(self):
        return f"{self.customer.username} - {self.product.name}"
    
class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart: {self.customer.username} - {self.product.name}"
    
# Order Model
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order: {self.customer.username} - {self.product.name}"