from django.db import models 
from logapp.models import Account
import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.db.models import Avg, Count 
from django.core.validators import RegexValidator
import random
# Create your models here.
class MainCategory(models.Model):
    id   = models.AutoField(primary_key=True)
    item = models.CharField(max_length=200, unique=True) 

    def __str__(self):
        return self.item

class Category(models.Model):
    title       = models.CharField(max_length=100,unique=True)
    category    = models.ForeignKey(MainCategory,on_delete=models.CASCADE,null=True) 
    # subcategory_image = models.ImageField(upload_to='category_image/',blank=True,null=True)
    # slug        = models.SlugField(max_length=255, unique=True)


    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse('category', args=[self.slug])





class Color(models.Model):
    name = models.CharField(max_length=50,unique=True)
    code = models.CharField(max_length=20,blank=True,null=True)
       
    def __str__(self):
       return self.name 

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p> style="background-color:{}">Color</p>'.format(self.code))

class Size(models.Model): 
    name    = models.CharField(max_length=50,unique=True)
    code    = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
       return self.name
#   Filter_Price = (
#         ('0 to 250','0 TO 250'),
#         ('250 TO 500','250 TO 500'),
#         ('500 TO 1000','500 TO 1000'),
#         ('1000 TO 2000','1000 TO 2000')
#     )

class Filter_Price(models.Model):
    price = models.CharField(max_length=50,default=0,unique=True)


    def __str__(self):
        return self.item

class Product(models.Model):
    id             = models.AutoField(primary_key=True)
    name           = models.CharField(max_length=100,unique=True)
    category       = models.ForeignKey(Category,on_delete=models.CASCADE)
    products_image = models.ImageField(upload_to='sell_image/',default='')
    price          = models.IntegerField(default=0)
    stock          = models.IntegerField(default=0)
    description    = models.TextField(max_length=1000,default='')
    user           = models.ForeignKey(Account,on_delete=models.CASCADE,default=1)
    # user          =models.ForeignKey(Account,on_delete=models.CASCADE,default=0)
    # slug          = models.SlugField(max_length=255,unique=True)
    # in_stock      = models.BooleanField(default=True)
    # is_active     = models.BooleanField(default=True)
    # publish       = models.DateTimeField(default=timezone.now)
    # updated       = models.DateTimeField(auto_now=True)

     
    @property
    def thumbnail_preview(self):
        if self.products_image:
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.products_image.url))
        return ""

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])

    def get_orders(self):
        orders = OrderPlaced.objects.filter(product=self)
        return orders
    
    
    def __str__(self):
       return self.name

    def get_url(self):
        return reverse('product_detail', args=[self.slug]) 




    # other fields as needed





class Cart(models.Model):
    user     = models.ForeignKey(Account,on_delete=models.CASCADE)
    product  = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=20,decimal_places=2,default=0) 
    size = models.ForeignKey(Size,on_delete=models.CASCADE,default=1)

    def get_product_price(self):
        price=[self.product.price]
        return sum(price)
    


class Wishlist(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user)


class OrderPlaced(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Shipped','Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),

    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    size = models.ForeignKey(Size,on_delete=models.CASCADE,default=1)
    quantity = models.IntegerField(default=1) 
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    otp = models.CharField(max_length=6,blank=True,null=True)
    is_ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_cost(self):
        return self.quantity

    def __str__(self):
        return str(self.user)     
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.otp:
            self.otp = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Requests(models.Model):
    STATUS = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, blank=True)
    request = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')

    def __str__(self):
        return self.topic

# class Complaint(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     message = models.CharField(max_length=100, blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)

class Query(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
  
class Sellerpayment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)





    def __str__(self):
        return str(self.user)


# class Seller_product(models.Model):
#     id            = models.AutoField(primary_key=True)
#     name          = models.CharField(max_length=100,unique=True)
#     category      = models.CharField(max_length=50)
#     size          = models.CharField(max_length=50)
#     color         = models.CharField(max_length=50)
#     # filterprice   = models.ForeignKey(Filter_Price, on_delete=models.CASCADE,default=1)
#     product_image = models.ImageField(upload_to='product_image/',unique=True)
#     price         = models.IntegerField(default=0)
#     stock         = models.IntegerField(default=0)
#     description   = models.TextField(max_length=1000,default='')
#     user          = models.ForeignKey(Account,on_delete=models.CASCADE,default=1)
    # user          =models.ForeignKey(Account,on_delete=models.CASCADE,default=0)
    # slug          = models.SlugField(max_length=255,unique=True)
    # in_stock      = models.BooleanField(default=True)
    # is_active     = models.BooleanField(default=True)
    # publish       = models.DateTimeField(default=timezone.now)
    # updated       = models.DateTimeField(auto_now=True)        

# class Sell_product(models.Model):
#     id            = models.AutoField(primary_key=True)
#     name          = models.CharField(max_length=100,unique=True)
#     category      = models.CharField(max_length=50)
#     products_image = models.ImageField(upload_to='sell_image/')
#     price         = models.IntegerField(default=0)
#     stock         = models.IntegerField(default=0)
#     description   = models.TextField(max_length=1000,default='')
#     user          = models.ForeignKey(Account,on_delete=models.CASCADE,default=1)

# class Productview(models.Model):
#     user=models.ForeignKey(Account,on_delete=models.CASCADE)
#     product=models.ForeignKey(Seller_product,on_delete=models.CASCADE)    