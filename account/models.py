from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Products(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    price=models.IntegerField()
    image=models.ImageField(upload_to="image")
    datetime=models.DateTimeField(auto_now=True)
    stock_options=(
        ("sale","sale"),
        ("soldout","soldout")
    )
    stock=models.CharField(max_length=100,choices=stock_options,default="sale")
    
    options=(
        ("Necklace","Necklace"),
        ("Earrings","Earrings"),
        ("Bangles","Bangles"),
        ("Anklets","Anklets"),
    )

    category=models.CharField(max_length=100,choices=options)
    def __str__(self):
        return self.title
    

class Cart(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now=True)
    quantity=models.IntegerField(default=1)


class Order(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now=True)
    quantity=models.IntegerField()
    options={
        ("OrderPlaced","OrderPlaced"),
        ("Shipped","Shipped"),
        ("OutForDelivery","OutForDelivery"),
        ("Delivered","Delivered"),
        ("Cancelled","Cancelled"),
    }
    status=models.CharField(max_length=100,default="OrderPlaced",choices=options)
    def __str__(self):
        return self.product.title
    

class ProductReview(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5) 
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.product.title} - {self.rating}"