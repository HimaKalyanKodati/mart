from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES = (
    ('VT','Vegitables'),
    ('FT','Fruits'),
    ('BI','Bathroom'),
    ('CL','Cloths'),
    ('EL','Electronics'),
    ('SH','Shoes'),
)

class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True

class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.IntegerField()
    dob = models.DateField(max_length=8)
    user_image = models.ImageField(upload_to='profile/images/', default='profile/images/default/default.jpg')
    
    
class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add1 = models.CharField(max_length=500)
    add2 = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=15)
    is_default = models.BooleanField(default=False)
    
class Category(BaseModel):
    name = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    description = models.TextField()
    def __str__(self) -> str:
        return self.name
    
class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sell_price = models.FloatField()
    mrp = models.FloatField()
    description = models.TextField()
    def __str__(self) -> str:
        return self.name
    
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/', default='product/images/default/default.jpg')
    
class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def get_total_price(self):
        return self.price * self.quantity
    
class WishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()