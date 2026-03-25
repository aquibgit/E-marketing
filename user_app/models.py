from django.db import models
from django.contrib.auth.models import User
from seller_app.models import Product

class user_details(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class Order(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255)
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default="PENDING")  # PENDING, PAID, CANCELLED
    status = models.CharField(max_length=20, default="Processing")  # Processing, Shipped, Delivered, Cancelled
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order {self.id}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} x {self.quantity}"
    

class Cart(models.Model):
    user = models.ForeignKey(
        'user_app.user_details',
        on_delete=models.CASCADE,
        null=True,     
        blank=True 
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
    
class Wishlist(models.Model):
    user = models.ForeignKey('user_app.user_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"
