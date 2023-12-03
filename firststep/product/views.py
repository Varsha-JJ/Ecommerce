from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product,Category,Size,Cart,Filter_Price,Color,Payment,OrderPlaced,Wishlist,ReviewRating,MainCategory,Requests,Sellerpayment,Query
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from logapp.models import Account
from django.conf import settings
import razorpay
from django.contrib import auth 

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# import speech_recognition as sr
# import pyaudio
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import base64
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.utils import timezone
import random
from django.template.loader import render_to_string
from django.http import JsonResponse 
import numpy as np
#customer segmentation 
# from mlxtend.preprocessing import TransactionEncoder
# from mlxtend.frequent_patterns import apriori
# from mlxtend.frequent_patterns import association_rules
import matplotlib
matplotlib.use('Agg') 
import networkx as nx
import io 
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd 

from django.db.models import Avg, Q
from django.core.exceptions import ObjectDoesNotExist

from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import csv 
from django.urls import reverse

# import plotly.graph_objs as go
import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from django.db.models import Count
import plotly.express as px

# Create your views here.
def product_detail(request,id):
    count = Cart.objects.filter(user=request.user.id).count()
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    sizes = Size.objects.all()
    review = ReviewRating.objects.filter(product_id=id, status=True)
    orderproduct = OrderPlaced.objects.filter(user=request.user.id, is_ordered=True).exists()
    # product = get_object_or_404(Product, id=id)
    # average_review = product.averageReview()
    # wishlist = Wishlist.object.filter(Q(product=product) & Q(user=request.user))
    products = Product.objects.get(id=id)
    cart = Cart.objects.all()
    wishlist = Wishlist.objects.all()
    product =  get_object_or_404(Product,id=id)
    average_review = product.averageReview()

    recomment = Product.objects.filter(reviewrating__rating__gte=4.0).annotate(avg_rating=Avg('reviewrating__rating')).order_by('-avg_rating')[:5]
    print(recomment)

    context = {
        'product': product,
        'review_count': product.countReview(),
        'averageReview' : average_review,
        'recomment' :recomment
    }
    return render(request,'product.html',{'recomment' :recomment,'product' : products,'size':sizes,'cart':cart,'wishlist':wishlist, 'count':count, 'w_count':w_count,'review':review, 'orderproduct':orderproduct,'context':context})


def filter_products(request):
    category_ids = request.GET.getlist('category[]')
    products = Product.objects.all()
    if category_ids:
        categories = Category.objects.filter(id__in=category_ids)
        products = products.filter(category__in=categories)
    data = [{'id': p.id, 'name': p.name, 'price': p.price} for p in products]
    return JsonResponse(data, safe=False)

def aboutus(request):
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    count = Cart.objects.filter(user=request.user.id).count()
    context = {
        'w_count':w_count,
        'count':count
    }
    return render(request,'aboutus.html',context)

def category(request,id):
    if( Category.objects.filter(id=id)):
        products   = Product.objects.filter(category_id=id)  
    else:
        messages.info(request, 'No Search Result!!!')
        print("No information to show")
    return render(request,'category.html',{'data':category,'product':products})

def size(request,id):
    if( Size.objects.filter(id=id)):
        products   = Product.objects.filter(size_id=id)  
    else:
        messages.info(request, 'No Search Result!!!')
        print("No information to show")
    return render(request,'size.html',{'product':products,'size':size})

def color(request,id):
    if(Color.objects.filter(id=id)):
        products   = Product.objects.filter(color_id=id)  
    else:
        messages.info(request, 'No Search Result!!!')
        print("No information to show")
    return render(request,'color.html',{'product':products,'color':color})

def price(request,id):
    if(Filter_Price.objects.filter(id=id)):
        products  = Product.objects.filter(filterprice_id=id)  
    else:
        messages.info(request, 'No Search Result!!!')
        print("No information to show")
    return render(request,'price.html',{'product':products,'filterprice':price})   

def subcategory(request):
    category = Category.objects.all()
    return render(request,'shop.html',{'category':category})    


def shop(request):
    count = Cart.objects.filter(user=request.user.id).count()    
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    maincate = MainCategory.objects.all()
    category = Category.objects.all()
    products = Product.objects.all()
    color = Color.objects.all()
    size = Size.objects.all()
    filterprice = Filter_Price.objects.all()
    # page = Paginator(products,6)
    # page_list = request.GET.get('page')
    # page = page.get_page(page_list)
    cart = Cart.objects.all()
    filterprice = Filter_Price.objects.all()
    # catid = request.GET.get('category')
    # maincat = request.GET.get('MainCategory')
    cateid = request.GET.get('Category')
    print("cateid:", cateid)
    maincate_id = request.GET.get('MainCategory')
    print("maincate_id",maincate_id)
    if maincate_id:
        category = Category.objects.filter(id=maincate_id)
        print("Filtered categories:",  category)
    else:
        category = Category.objects.all()
    # selpro = Sell_product.objects.all()
    if cateid:
        products = Product.objects.filter(category_id=cateid)
        print("Filtered products:", products)
    else:
        products = Product.objects.all()
    return render(request,'shop.html',{'maincate':maincate,'data':category,'products':products,'color':color,'filterprice':filterprice,'size':size,'count':count,'w_count':w_count})   

def girls(request):
    products = Product.objects.filter() 
    # {'product':product}
    count = Cart.objects.filter(user=request.user.id).count()
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    context = {
        'count':count,
        'w_count':w_count,
        'products':products
    }
    return render(request,'girls.html',context) 


def boys(request):
    count = Cart.objects.filter(user=request.user.id).count()
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    context = {
        'count':count,
        'w_count':w_count
    }
    return render(request,'boys.html',context) 
          



def wishlist(request):
    count = Cart.objects.filter(user=request.user.id).count()
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    return render(request,'wishlist.html',{'wish':wish,'count':count,'w_count':w_count})  
           

def sample(request):
    return render(request,'sample.html')    

def searchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(price__icontains=query) | Q(description__icontains=query))
            products = Product.objects.filter(multiple_q) 
            return render(request, 'searchbar.html', {'product':products})
        else:
            messages.info(request, 'No Search Result!!!')
            print("No information to show")
    return render(request, 'searchbar.html', {}) 



#Add to Cart.
@login_required(login_url='login')
def addcart(request,id):
      user = request.user 
      s = Size.objects.all()
      item=Product.objects.get(id=id)
      if request.method == 'POST':
        size_id = request.POST.get('size') 
        print("size_id",size_id) 
        size = Size.objects.get(id=size_id)
        if item.stock>0:
            if Cart.objects.filter(user_id=user,product_id=item,size=size).exists():
                return redirect(cart)
            else:
                product_qty=1
                price=item.price * product_qty
                new_cart=Cart(user_id=user.id,product_id=item.id,product_qty=product_qty,price=price,size=size,)
                new_cart.save()
                return redirect(shop)
                



# Cart Quentity Plus Settings
def plusqty(request,id):
    cart=Cart.objects.filter(id=id)
    for cart in cart:
        if cart.product.stock > cart.product_qty:
            cart.product_qty +=1
            cart.price=cart.product_qty * cart.product.price
            cart.save()
            return redirect('cart')
        # messages.success(request, 'Out of Stock')
        return redirect('cart')

# Cart Quentity Plus Settings
def minusqty(request,id):
    cart=Cart.objects.filter(id=id)
    for cart in cart:
        if cart.product_qty > 1 :
            cart.product_qty -=1
            cart.price=cart.product_qty * cart.product.price
            cart.save()
            return redirect('cart')
        return redirect('cart')



# View Cart Page
@login_required(login_url='login')
def cart(request):
    # totalitem = 0
    # if request.user.is_authenticated :
    #     totalitem = len(Cart.objects.filter(user = request.user)) 

    w_count = Wishlist.objects.filter(user=request.user.id).count()
    count = Cart.objects.filter(user=request.user.id).count()
    user = request.user
    cart=Cart.objects.filter(user_id=user)
    total=0
    for i in cart:
        total += i.product.price * i.product_qty 
        # Reduce the stock count of the item by the quantity in the cart
        # i.product.stock -= i.product_qty
        # i.product.save()
    category=Category.objects.all()
    # subcategory=Subcategory.objects.all()
    return render(request,'cart.html',{'cart':cart,'total':total,'category':category,'count':count,'w_count':w_count})

# Remove Items From Cart
def de_cart(request,id):
    Cart.objects.get(id=id).delete()
    return redirect(cart)




@login_required(login_url='login')
def checkout_update(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('addres')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        password = request.POST.get('password')
        user_id = request.user.id

        user = Account.objects.get(id=user_id)
        user.first_name = fname
        user.last_name = lname
        user.address = address
        user.email = email
        user.contact = phone
        user.city = city
        user.state = district
        user.pincode = pincode


        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Updated Successfully')
        return redirect('checkout')

def checkout(request):
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    count = Cart.objects.filter(user=request.user.id).count()
    user = request.user
    cart=Cart.objects.filter(user_id=user)
    total=0
    for i in cart:
        total += i.product.price * i.product_qty 
        # Reduce the stock count of the item by the quantity in the cart
        # i.product.stock -= i.product_qty
        # i.product.save()
    category=Category.objects.all()
    razoramount = total*100
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET_KEY))
    data = {
        "amount": total,
        "currency": "INR",
        "receipt": "order_rcptid_11"
    }
    payment_response = client.order.create(data=data)
    print(payment_response)
    # {'id': 'order_KiECe57gQjLLKg', 'entity': 'order', 'amount': 400, 'amount_paid': 0, 'amount_due': 400, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1668933116}
    order_id = payment_response['id']
    request.session['order_id'] = order_id
    order_status = payment_response['status']
    if order_status == 'created':
        payment = Payment(
            user=request.user,
            amount=total,
            razorpay_order_id = order_id,
            razorpay_payment_status = order_status
            )
        payment.save()
    return render(request,'checkout.html',{'cart':cart,'total':total,'category':category,'razoramount':razoramount,'count':count,'w_count':w_count})   

#delivery
def send_order_confirmation_email(order):
    otp_code = order.otp
    user = order.user
    email_body = render_to_string('order_confirmation_email.html', {'order': order, 'otp_code': otp_code})

    message = render_to_string('order_confirmation_email.html', {
        'user': user,
        'otp_code': otp_code,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'email_body': email_body
    })

    send_mail(
        'Order Confirmation and OTP',
        message,
        'onlinefirststep1@gmail.com',
        [user.email],
        fail_silently=False,
    )



def payment_done(request):
    order_id=request.session['order_id']
    payment_id = request.GET.get('payment_id')
    print(payment_id)

    payment=Payment.objects.get(razorpay_order_id = order_id)

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    # customer=Address_Book.objects.get(user=request.user,status=True)

    cart=Cart.objects.filter(user=request.user)
    # item = Product.objects.get(product=product, id=item_id)

    for c in cart:
        otp_code = str(random.randint(100000, 999999))
        # decrease stock based on quantity ordered
        order=OrderPlaced(user=request.user,product=c.product,size=c.size,quantity=c.product_qty,payment=payment, otp=otp_code,is_ordered=True)
        order.save()
        send_order_confirmation_email(order)
        c.product.stock -= c.product_qty
        c.product.save()
        c.delete()
    return redirect('showbill')

@login_required(login_url='login')
def add_wishlist(request,id):
    user = request.user
    item=Product.objects.get(id=id)
    if Wishlist.objects.filter( user_id =user,product_id=item).exists():
        messages.success(request, 'Already in the wishlist ')
        return redirect('shop')
    else:
            new_wishlist=Wishlist(user_id=user.id,product_id=item.id)
            new_wishlist.save()
            messages.success(request, 'Product added to the wishlist ')
            return redirect('shop')
    # messages.success(request, 'Sign in..!!')
    # return redirect(index)


#Wishlist View page
@login_required(login_url='login')
def view_wishlist(request):
        count = Cart.objects.filter(user=request.user.id).count()
        w_count = Wishlist.objects.filter(user=request.user.id).count()
        user = request.user
        wish=Wishlist.objects.filter(user_id=user)
        # Get a list of all product IDs in the user's wishlist
        wishlist_ids = [w.product_id for w in wish]
        category=Category.objects.all()
        return render(request,"wishlist.html",{ 'wishlist_ids': wishlist_ids,'wishlist':wish,'category':category,'wish':wish,'count':count,'w_count':w_count})


# Remove Items From Wishlist
def de_wishlist(request,id):
    Wishlist.objects.get(id=id).delete()
    return redirect('view_wishlist')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def get(request,id,*args, **kwargs,):
        
        place = OrderPlaced.objects.get(id=id)
        date=place.payment.created_at

        orders=OrderPlaced.objects.filter(user_id=request.user.id,payment__created_at=date)
        total=0
        for o in orders:
            total=total+(o.product.price*o.quantity)
        addrs=Account.objects.get(id=request.user.id)
     
        #     print(i.user,"#######################")
        data = {
            "total":total,
            "orders":orders,
            "shipping":addrs,
    
 
        }
        pdf = render_to_pdf('report.html',data)
        if pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            # filename = "Report_for_%s.pdf" %(data['id'])
            filename = "Bill.pdf"

            content = "inline; filename= %s" %(filename)
            response['Content-Disposition']=content
            return response
        return HttpResponse("Page Not Found") 

@login_required(login_url='login')
def showbill(request):
    count = Cart.objects.filter(user=request.user.id).count() 
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    orders = OrderPlaced.objects.filter(
        user=request.user, is_ordered=True).order_by('ordered_date')
    context = {
        'orders': orders,
        'count':count,
        'w_count':w_count
    }
    return render(request, "showbill.html",context)



#ADMIN FUNCTIONS
# @login_required(login_url='login')
# def index(request):
#     user = request.user
#     new_orders_count = OrderPlaced.objects.filter(is_ordered=True, product__user=user).count()
#     return render(request, "seller/index.html",{'new_orders_count': new_orders_count})



def forms(request):
     return render(request, "seller/forms.html")

@login_required(login_url='login')
def profile(request):
    return render(request, "seller/profile.html")

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    new_orders_count = OrderPlaced.objects.filter(is_ordered=True, product__user=user).count()
    return render(request, "seller/dashboard.html",{'new_orders_count': new_orders_count})


# def category(request):
#      return render(request, "seller/category.html")

# def subcategory(request):
#      return render(request, "seller/subcategory.html")
@login_required(login_url='login')
def product(request):
    cat = Category.objects.all()
    color = Color.objects.all()
    size = Size.objects.all()
    user = request.user
    if request.method == "POST":
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        pname = request.POST.get('pname')
        pdesc = request.POST.get('pdesc')
        pimg = request.FILES.get('pimg')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        existing_product = Product.objects.filter(user=user, name=pname).first()
        if existing_product:
            messages.warning(request, 'Product with this name already exists.')
        else:
            val = Product(user=user, category=category, name=pname, description=pdesc, price=price, stock=stock)
            if pimg:
                val.products_image = pimg
            try:
                val.full_clean()
                val.save()
                messages.success(request, 'Product added successfully.')
            except ValidationError as e:
                messages.error(request, e.message_dict)
    return render(request, "seller/product.html", {'cat': cat, 'color': color, 'size': size})    


@login_required(login_url='login')
def viewsellpro(request,id):
    products = Product.objects.get(id=id)

    context = {
        'products':products,
    }
    return render(request,'seller/viewsellpro.html',context)

@login_required(login_url='login')
def table(request):
    user = request.user
    products = Product.objects.filter(user_id=user)
    for product in products:
        if product.stock < 5:
            messages.warning(request,f"Stock of {product.name} is below 5!!!!")
    return render(request, "seller/tables.html",{'products':products})


def product_detailslog(request):
    user = request.user
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productdetail.csv"'
    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Price', 'Image', 'Stock'])
    order_details =  products = Product.objects.filter(user_id=user).values_list('name', 'price','products_image', 'stock')
    for i in order_details:
        writer.writerow(i)
    return response



# def viewproduct(request):
#     user = request.user.id
#     products = Seller_product.objects.all(userid=user)
#     return render(request,"seller/tables.html")    



@login_required(login_url='login')
def productedit(request,id):
    cat = Category.objects.all()
    products = Product.objects.get(id=id)

    context = {
        'products':products,
        'data':cat
    }
    # cat = Category.objects.all()
  
   
    # if request.method == "POST":
    #     cate = request.POST.get('cate')
    #     pname = request.POST.get('pname')
    #     pdesc = request.POST.get('pdesc')
    #     pimg = request.POST.get('pimg')
    #     price = request.POST.get('price')
    #     stock = request.POST.get('stock')
        
    #     pro = Seller_product.objects.get(id=id)
    #     pro.category = cate 
    #     pro.name = pname 
    #     pro.descrition = pdesc 
    #     pro.product_image = pimg 
    #     pro.price = price 
    #     pro.stock = stock 

    #     pro.save()
        # {'data':cat,'color':color,'size':size}    
    return render(request, "seller/productedit.html",context) 

@login_required(login_url='login')
def productupdate(request):
    cat = Category.objects.all()
    if request.method == "POST":
        products_id = request.POST.get('products_id')
        # category_id = request.POST.get('category') 
        # print("category_id:", category_id)
        # category = Category.objects.get(id=category_id)
        # pname = request.POST.get('pname')
        pdesc = request.POST.get('pdesc')
        # pimg = request.FILES['pimg']
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        # Check if the product already exists
        try:
            value = Product.objects.get(id=products_id)
            messages.warning(request,f"{product_name} already exists.")
        except Product.DoesNotExist: 
            # Update the product details
            value.price = price
            value.stock = stock
            value.description = pdesc
            value.save()   
            # Show success message
            messages.success(request, 'Product details have been updated successfully.')
    
            # value.category = category
            # value.name = pname
            # value.products_image = pimg
            # value.price = price
            # value.stock = stock
            # value.description = pdesc
            # value.save()
        return redirect('table')

        print(cate,pname,pdesc,pimg,price,stock)
    return render(request, "seller/productedit.html")

@login_required(login_url='login')
def deleteproduct(request,id):
    try:
        item  = Product.objects.get(id=id)
        item.delete()
        messages.success(request, f" {item.name} has been deleted.")
    except Product.DoesNotExist:
        messages.warning(request, "The product you are trying to delete does not exist.")
    return redirect('table') 


from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime, timedelta
@login_required(login_url='login')
def sellorders(request):
    user = request.user
    today = datetime.now()
    start_date = datetime(today.year, today.month, 1)
    end_date = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1]) + timedelta(days=1)
    
    # Get all the unique months for which the user has placed orders
    unique_months = OrderPlaced.objects.filter(is_ordered=True, product__user=user).\
        datetimes('ordered_date', 'month').\
        order_by('-ordered_date__month').\
        distinct('ordered_date__month')
    
    # Create a dictionary to hold the data for each month
    monthly_data = {}
    for month in unique_months:
        orders = OrderPlaced.objects.filter(is_ordered=True, product__user=user,
                                             ordered_date__month=month.month, ordered_date__year=month.year)
        total_amount = orders.aggregate(Sum('product__price'))['product__price__sum'] or 0
        total_amount_quarter = int(total_amount / 4)
        print("total_amount_quarter",total_amount_quarter)
        earning = total_amount - total_amount_quarter
        print("earning",earning)
        is_paid = Sellerpayment.objects.filter(user=user, paid=True,
                                               razorpay_payment_status='created',
                                               razorpay_order_id__startswith=f'{month.year}{month.month}',
                                               ).exists()
       
        razoramount = total_amount_quarter 
        print("razoramount",razoramount)

        # Check if payment button should be enabled
        end_of_month = datetime(today.year, today.month, 1) + relativedelta(months=1) - relativedelta(days=1)
        if datetime.now() > end_of_month:
            is_payment_enabled = True
        else:
            is_payment_enabled = False

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
        data = {"amount": razoramount, "currency": "INR",
                "receipt": "order_rcptid_11"}
        print("data",data)        
        payment_response = client.order.create(data=data)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Sellerpayment(
                user=request.user,
                amount=total_amount_quarter,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
            )
            payment.save()
            print('payment',payment)

        context = {
            'orders': orders,
            'total_amount': total_amount,
            'total_amount_quarter': total_amount_quarter,
            'razoramount': razoramount,
            'is_paid': is_paid,
            'is_payment_enabled': is_payment_enabled,
            'earning': earning,
            'month_name': month.strftime("%B %Y"),
            'has_orders': orders.exists()
        }

        # Add the data for this month to the monthly_data dictionary
        monthly_data[month.strftime("%B %Y")] = context

    return render(request, 'seller/sellorders.html', {'monthly_data': monthly_data})

def initiate(request):
    order_id=request.session['order_id']
    payment_id = request.GET.get('payment_id')
    print(payment_id)

    payment=Sellerpayment.objects.get(razorpay_order_id = order_id)
    # razorpay_payment_id = request.POST.get('razorpay_payment_id')
    # razorpay_payment_status = request.POST.get('razorpay_payment_status')
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save() 
    return redirect('pay')

def pay(request):
    return render(request,'seller/pay.html')



#sellerayment
# def initiate(request):
#     if request.method == 'POST':
#         payment_id = request.POST.get('payment_id')
#         razorpay_payment_id = request.POST.get('razorpay_payment_id')
#         razorpay_payment_status = request.POST.get('razorpay_payment_status')
#         # amount = Decimal(request.POST.get('amount'))
#         amount = request.POST.get('amount')
#         print('init amount',amount)
#         client = razorpay.Client(auth=('rzp_test_ou7rNcgJfkqsyG', '0XWzrdn5mNWzarL1dWpgMV7B'))
#         payment = client.order.fetch(payment_id)

#         if razorpay_payment_status == 'captured':
#             payment_status = True
#         else:
#             payment_status = False

#         Sellerpayment.objects.create(user=request.user, amount=amount, razorpay_payment_id=razorpay_payment_id, razorpay_payment_status=razorpay_payment_status, paid=payment_status)

#         messages.success(request, 'Payment Successful')
#         return redirect('sellorders')







import csv

def order_detailslog(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orderdetail.csv"'
    writer = csv.writer(response)
    writer.writerow(['User name','Address','Pincode','Product name','Quantity'])
    order_details =  OrderPlaced.objects.all().values_list('user__first_name','user__address','user__pincode','product__name','quantity')
    for i in order_details:
        writer.writerow(i)
    return response

def sellrequest(request):
    if request.method == 'POST':
        user = request.user
        topic = request.POST.get('category')
        request_data = request.POST.get('pdesc')
       
        new_request = Requests(user=user, topic=topic, request=request_data)
        new_request.save()
        
        messages.success(request, 'Your request has been successfully sent!')
        return redirect('sellrequest') # redirect to a success page or another view
    else:
        return render(request, 'seller/sellrequest.html') # render the form template


def sellviewrequest(request):
    req = Requests.objects.all()
    print("req",req)
    return render(request, 'seller/sellviewrequest.html',{'req':req})


def reviewss(request,id):
        if request.method == 'POST':
            try:
                reviews = ReviewRating.objects.get(user_id=request.user.id, product_id=id)
                subject = request.POST.get('subject')
                rating = request.POST.get('rating')
                review = request.POST.get('review')
                reviews.subject = subject
                reviews.rating = rating
                reviews.review = review
                reviews.save()
                messages.success(request, 'Thank you! Your review has been updated.')
                return redirect(request.META.get('HTTP_REFERER'))
            except ReviewRating.DoesNotExist:
                subject = request.POST.get('subject')
                rating = request.POST.get('rating')
                review = request.POST.get('review')
                data = ReviewRating()
                data.subject = subject
                data.rating = rating
                data.review = review
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = id
                data.user_id = request.user.id
                if OrderPlaced.objects.filter(user_id=request.user.id, product_id=id, is_ordered=True).exists():
                    data.save()
                    messages.success(request, 'Thank you! Your review has been submitted.')
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.warning(request, 'You can only review products that you have purchased.')
                    return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('/')


@login_required(login_url='login')
def sellreview(request):
    user = request.user
    user_id=user.id
    review = ReviewRating.objects.filter(product__user=user)
    return render(request,'seller/sellreview.html',{'reviews':review})



from django.db.models.functions import TruncMonth
@login_required(login_url='login')
def index(request):
    user = request.user
    new_orders_count = OrderPlaced.objects.filter(is_ordered=True, product__user=user).count()
    prod = Product.objects.filter(user_id=user).count()
    amount = OrderPlaced.objects.filter(is_ordered=True, product__user=user)
    Revenue = 0
    for i in amount:
        Revenue += i.product.price
    print("Revenue",Revenue)

        # Get all orders placed by customers
    # orders = OrderPlaced.objects.filter(is_ordered=True, product__user=user)

    # # Create a list of all unique customers
    # customers = list(set([order.user for order in orders]))

    # # Create a dictionary to store customer purchase history
    # purchase_history = {customer.id: {'total_spent': 0, 'num_orders': 0} for customer in customers}

    # # Calculate each customer's total spending and number of orders
    # for order in orders:
    #     purchase_history[order.user.id]['total_spent'] += order.product.price * order.quantity
    #     purchase_history[order.user.id]['num_orders'] += 1

    # # Convert the purchase history dictionary to a pandas dataframe
    # df = pd.DataFrame.from_dict(purchase_history, orient='index')

    # # Scale the data
    # scaler = StandardScaler()
    # scaled_data = scaler.fit_transform(df)

    # # Perform KMeans clustering
    # kmeans = KMeans(n_clusters=1, random_state=0).fit(scaled_data)

    # # Add cluster labels to customers
    # customer_clusters = {customer.id: kmeans.labels_[i] for i, customer in enumerate(customers)}

    # # Create a scatter plot of total spending vs. number of orders, colored by cluster
    # plt.figure()
    # plt.scatter(df['total_spent'], df['num_orders'], c=[customer_clusters[customer.id] for customer in customers])
    # plt.xlabel('Total Spending')
    # plt.ylabel('Number of Orders')
    # plt.title('Customer Segmentation')

    # # Convert the plot to a Django response
    # buffer = BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    # image_png = buffer.getvalue()
    # buffer.close()
    # customer_graphic = base64.b64encode(image_png)
    # customer_graphic = customer_graphic.decode('utf-8')

    user = request.user.id
    products = Product.objects.filter(user_id=user)
    purchase_history = {product.name: 0 for product in products}
    orders = OrderPlaced.objects.filter(is_ordered=True,product__user=user)
    for order in orders:
        purchase_history[order.product.name] += order.quantity

    # Sort the products by purchase count
    sorted_products = sorted(purchase_history.items(), key=lambda x: x[1], reverse=True)

    # Create lists of the product names and purchase counts
    product_names = [item[0] for item in sorted_products]
    purchase_counts = [item[1] for item in sorted_products]

    # Create a bar chart of the product purchase counts
    fig = go.Figure(data=[go.Bar(x=product_names, y=purchase_counts)])
    fig.update_layout(title='Most Purchased Products', xaxis_title='Product Name', yaxis_title='Purchase Count')
    graph_div = fig.to_html(full_html=False)



    #sales in month
    # Get the monthly sales data for the product
    monthly_sales = OrderPlaced.objects.filter( is_ordered=True)\
        .annotate(month=TruncMonth('ordered_date'))\
        .values('month')\
        .annotate(total_sales=Count('id'))\
        .order_by('month')

    # Create the x and y axis data for the plot
    x_axis = [sale['month'] for sale in monthly_sales]
    y_axis = [sale['total_sales'] for sale in monthly_sales]

    # Create the plot layout
    plot_layout = go.Layout(
        title='Monthly Sales for Product',
        xaxis=dict(title='Month'),
        yaxis=dict(title='Total Sales')
    )

    # Create the plot data
    plot_data = [go.Scatter(x=x_axis, y=y_axis, mode='lines+markers')]

    # Create the plot figure
    plot_fig = go.Figure(data=plot_data, layout=plot_layout)

    # Render the plot using Plotly's HTML renderer
    plot_html = plot_fig.to_html(full_html=False)


     












#     Create a bar chart of the most purchased items 
#     er = request.user.id
#     products = Product.objects.filter(user_id=user)
#     purchusase_history = {product.name: 0 for product in products}
#     orders = OrderPlaced.objects.filter(is_ordered=True,product__user=user)
#     for order in orders:
#         purchase_history[order.product.name] += order.quantity

#     # Sort the products by purchase count
#     sorted_products = sorted(purchase_history.items(), key=lambda x: x[1], reverse=True)

#     # Create lists of the product names and purchase counts
#     product_names = [item[0] for item in sorted_products]
#     purchase_counts = [item[1] for item in sorted_products]

#    # Create a bar chart of the product purchase counts
#     fig, ax = plt.subplots(figsize=(10, 6))  # Increase the figure size
#     y_pos = np.arange(len(product_names))
#     colors = ['#E6DAA6', '#E6DAA6', '#E6DAA6', '#E6DAA6', '#E6DAA6', '#E6DAA6', '#E6DAA6']  # Create a list of colors
#     plt.figure()
#     plt.bar(y_pos, purchase_counts, align='center', color=colors[:len(product_names)])  # Use colors for each bar
#     plt.xticks(y_pos, product_names, rotation='vertical',fontsize=6)
#     plt.xlabel('Product Name')
#     plt.ylabel('Purchase Count')
#     plt.title('Most Purchased Products')

#     # Convert the plots to Django responses
#     buffer1 = BytesIO()
#     plt.savefig(buffer1, format='png')
#     buffer1.seek(0)
#     image_png1 = buffer1.getvalue()
#     buffer1.close()
#     most_purchased_graphic = base64.b64encode(image_png1)
#     most_purchased_graphic = most_purchased_graphic.decode('utf-8')
    

    context = {
    'new_orders_count': new_orders_count,
    # 'customer_graphic': customer_graphic,
    # 'most_purchased_graphic':most_purchased_graphic,
    'Revenue':Revenue,
    'prod':prod,
    'graph_div': graph_div,
    'plot_html': plot_html

    }
    return render(request, 'seller/index.html',context)




@login_required(login_url='login')
def market_basket_analysis(request):
    user = request.user
     # Load data
    orders = OrderPlaced.objects.filter(is_ordered=True, product__user=user)

    # Convert data to transaction format
    transactions = {}
    for order in orders:
        if order.user not in transactions:
            transactions[order.user] = []
        transactions[order.user].append(order.product.name)
    print(transactions)  # print transactions for debugging
    # Perform market basket analysis
    te = TransactionEncoder()
    te_ary = te.fit(list(transactions.values())).transform(list(transactions.values()))
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
    print(frequent_itemsets)  # print frequent itemsets for debugging
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    print(rules)
    # Render template with association rules


    
    return render(request, 'seller/market_basket_analysis.html', {'rules': rules})


    



def users(request):
    user = request.user
    products = Product.objects.filter(user_id=user)
    return render(request,'seller/users.html',{'products':products})









def search_by_voice(request):
    if request.method == 'POST':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            # save query to database
            # perform search and retrieve results
            return render(request, 'search_results.html', {'results': results})
        except sr.UnknownValueError:
            return HttpResponse("Unable to recognize speech")
        except sr.RequestError as e:
            return HttpResponse("Error: {}".format(e))
    else:
        return render(request, 'search_by_voice.html')



def graph(request):
    
    return render(request, 'seller/graph.html')










#DELIVERY AGENT


def deliveryindex(request,id):
    products = OrderPlaced.objects.get(id=id)
    context = {
        'products':products
    }
    return render(request,'delivery/deliveryindex.html',context)

def deliveryorder(request):
    order = OrderPlaced.objects.exclude(status='Delivered')
    context = {
        'order':order
    }
    return render(request,'delivery/deliveryorder.html',context)

def deliveryproview(request,id):
    products = OrderPlaced.objects.get(id=id)
    order = get_object_or_404(OrderPlaced, id=id, status='Pending')
    print(order.status)
    print(order.otp)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        print(entered_otp)
        if entered_otp == order.otp:
            order.status = 'Delivered'
            order.is_ordered = True
            order.save()
            print(order.status)
            return redirect('deliveryconfrim')
        else:
          messages.warning(request, 'Invalid OTP. ')
    context = {
        'products':products,
        'order':order
    }
    return render(request,'delivery/deliveryproview.html',context)

def deliveryprofile(request):
    return render(request,'delivery/deliveryprofile.html')

def deliveryconfrim(request):
    return render(request,'delivery/deliveryconfrim.html')

def verify(request):
    return render(request,'delivery/verify.html')

#ADMIN PAGE
@login_required(login_url='login')
def admin_dashboard(request):
    
    custom =  Account.objects.filter(is_active=True,is_user=True).count()
    seller = Account.objects.filter(is_staff=True, is_active=True,is_superuser=False,approved_delivery=False,approved_staff=True).count()
    products_count = Product.objects.count()
    latest_active_staff_users = Account.objects.filter(is_staff=True, is_active=True,is_superuser=False,approved_delivery=False,approved_staff=True,date_joined__lte=timezone.now(),).order_by('-date_joined')[:2]  # get the latest 10 users
    count_latest = latest_active_staff_users.count()
  
    # Get the number of sellers joined each week
    data = Account.objects.filter(is_staff=True, is_active=True).extra({'week': "EXTRACT(WEEK FROM date_joined)"}).values('week').annotate(count=Count('id')).order_by('week')

    # Extract the week numbers and counts from the data
    weeks = [d['week'] for d in data]
    counts = [d['count'] for d in data]

    # Create a Plotly bar chart with the data
    fig = go.Figure(
        data=[go.Bar(x=weeks, y=counts)],
        layout=go.Layout(
            title=go.layout.Title(text="Number of Sellers Joined Each Week"),
            xaxis=go.layout.XAxis(title="Week Number"),
            yaxis=go.layout.YAxis(title="Number of Sellers")
        )
    )
    
    # Create a donut graph using Plotly
    sellers = Account.objects.filter(is_staff=True, is_active=True, product__orderplaced__is_ordered=True)
    product_count = sellers.annotate(product_count=Count('product__orderplaced')).values('first_name', 'product_count')
    seller_dict = {seller['first_name']: seller['product_count'] for seller in product_count}
    sorted_seller_dict = dict(sorted(seller_dict.items(), key=lambda item: item[1], reverse=True))
    seller_names = list(sorted_seller_dict.keys())
    product_counts = list(sorted_seller_dict.values())
    donut_fig = go.Figure(data=[go.Pie(labels=seller_names, values=product_counts, hole=.3)])
    donut_graph_html = donut_fig.to_html(full_html=False)

    context = {
        'custom': custom,
        'seller': seller,
        'count_latest':count_latest,
        'products_count': products_count,
        'graph': fig.to_html(full_html=False),
        'donut_graph_html': donut_graph_html
    }
    return render(request,'admin/admin_dashboard.html',context)


@login_required(login_url='login')
def admin_user(request):
    custom =  Account.get_active_users()
    context = {
        'custom' : custom
    }
    return render(request,'admin/admin_user.html',context)

@login_required(login_url='login')
def admin_seller(request):
    seller = Account.get_active_staff_users()
    # Get the latest active seller
    latest_seller = Account.get_active_staff_users().order_by('-date_joined').first()

    # Check if the latest active seller joined recently
    if latest_seller and latest_seller.date_joined >= timezone.now() - timezone.timedelta(days=7):
        # If so, create a warning message
        warning_message = f"The latest seller {latest_seller.first_name} joined recently. Please review their account."

        # Add the warning message to the messages framework
        messages.warning(request, warning_message)
    print("seller",seller)
    context = {
        'seller': seller
        }
    return render(request,'admin/admin_seller.html',context)    



def seller_detailslog(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sellerdetail.csv"'
    writer = csv.writer(response)
    writer.writerow(['Seller Name', 'Address', 'Contact', 'City', 'State', 'Pincode'])
    order_details =  Account.objects.filter(is_staff=True, is_active=True).values_list('first_name', 'address', 'contact', 'city', 'state', 'pincode')
    for i in order_details:
        writer.writerow(i)
    return response




@login_required(login_url='login')
def admin_sellerapprove(request,id):
    user = Account.objects.get(id=id)
    
    context = {
        'user':user
    }
    return render(request,'admin/admin_sellerapprove.html',context) 

@login_required(login_url='login')
def admin_approveupdate(request):
    if request.method == 'POST':
        user_id = request.POST.get('useid')
        user = Account.objects.get(id=user_id)
        
        approve = request.POST.get('approve')
        prev_approve = request.POST.get('prev_approve')
        
        if approve == 'on':
            user.approved_staff = True
            messages.success(request, 'Seller approved successfully.')
        elif prev_approve == 'True':
            user.approved_staff = False
            messages.success(request, 'Seller unapproved successfully.')
            
        user.save()
       
    return redirect(reverse('admin_sellerapprove', kwargs={'id': user_id}))


@login_required(login_url='login')
def admin_delivery(request):
    delivery = Account.active_users_with_staff_role()
    print("delivery",delivery)
    return render(request,'admin/admin_delivery.html',{'delivery':delivery})    

@login_required(login_url='login')
def admin_adddelivery(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        district = request.POST.get('state')
        pincode = request.POST.get('pincode')
        approve = request.POST.get('approve')

        if Account.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
        else:
            user = Account(first_name=fname,last_name=lname,address=address,email=email,contact=phone,city=city,state=district,pincode=pincode)
            user.is_active = True
            user.is_user = True
            user.is_staff=True 
            if approve == 'on':
                user.approved_delivery = True  # set approved_delivery to True if checkbox is checked
            user.save() 
            messages.success(request, 'Delivery boy added successfully')           

    return render(request,'admin/admin_adddelivery.html') 

@login_required(login_url='login')
def deliverydel(request,id):
    users = Account.objects.get(id=id)
    users.delete()
    messages.success(request, 'Delivery boy deleted successfully')
    return redirect('admin_delivery')


@login_required(login_url='login')
def admin_addcategory(request):  
    if request.method == "POST":
        categories = request.POST.get('cates')

        value = MainCategory(item=categories)
        value.save()
        print("categories",categories)
        messages.success(request, 'Category added successfully')
    return render(request, 'admin/admin_addcategory.html')




@login_required(login_url='login')
def admin_viewcategory(request):
    main = MainCategory.objects.all()  
    context = {
        'main': main
    }
    return render(request,'admin/admin_viewcategory.html', context)

def admin_categoryedit(request,id):
    maincat = MainCategory.objects.get(id=id)
    print("maincat",maincat)
       # cates = Category.objects.get(id=id)
    return render(request,'admin/admin_categoryedit.html',{'maincat':maincat})


def admin_categoryupdate(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        cate_name = request.POST.get('cates')
        print("cate_name",cate_name)
        value = MainCategory.objects.get(id=category_id)
        old_title = value.item
        value.item = cate_name
        value.save()
        messages.success(request,f"{old_title} has been updated.")
    return redirect('admin_viewcategory')

@login_required(login_url='login')
def admin_categorydelete(request,id):
    try:
        cate  = MainCategory.objects.get(id=id)
        cate.delete()
        messages.success(request, f" {cate.item} has been deleted.")
    except MainCategory.DoesNotExist:
        messages.warning(request, "The category you are trying to delete does not exist.")
    return redirect('admin_viewcategory')

@login_required(login_url='login')
def admin_subaddcategory(request):
    cat = MainCategory.objects.all()
    if request.method == "POST":
        cate_name = request.POST.get('cate_name')
        category_id = request.POST.get('category') 
        print("category_id:", category_id)
        category = MainCategory.objects.get(id=category_id)
        
        try:
            existing_category = Category.objects.get(title=cate_name, category=category)
            messages.warning(request, 'Category already exists')
        except ObjectDoesNotExist:
            new_category = Category(title=cate_name, category=category)
            new_category.save()
            messages.success(request, 'Category added successfully')
            
    return render(request,'admin/admin_subaddcategory.html',{'cat':cat})

@login_required(login_url='login')
def admin_deletesub(request,id):
    try:
        item  = Category.objects.get(id=id)
        item.delete()
        messages.success(request, f" {item.title} has been deleted.")
    except Category.DoesNotExist:
        messages.warning(request, "The sub-category you are trying to delete does not exist.")
    return redirect('admin_subviewcategory')



@login_required(login_url='login')
def admin_subviewcategory(request):
    category = Category.objects.all()
    context = {
        'category' : category
    }
    return render(request,'admin/admin_subviewcategory.html',context)    

@login_required(login_url='login')
def admin_editsub(request,id):
    mainn = MainCategory.objects.all()
    cates = Category.objects.get(id=id)
    context = {
        'cates':cates,
        'mainn':mainn
    }

    return render(request,'admin/admin_editsub.html',context) 

@login_required(login_url='login')
def admin_updatesub(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        cate_name = request.POST.get('cate_title')
        print("cate_name",cate_name)
        value = Category.objects.get(id=category_id)
        old_title = value.title
        value.title = cate_name
        value.save()
        messages.success(request,f"{old_title} has been updated.")
        return redirect('admin_subviewcategory')
    return render(request,'admin/admin_editsub.html') 


@login_required(login_url='login')
def admin_addproduct(request):
    return render(request,'admin/admin_addproduct.html')            


@login_required(login_url='login')
def admin_viewproduct(request,id):
    product = Product.objects.get(id=id)
    return render(request,'admin/admin_viewproduct.html',{'product':product})

@login_required(login_url='login')
def admin_addsize(request):
    size = Size.objects.all()
    if request.method == "POST":
        size_name = request.POST.get('size')
        try:
            size_obj = Size.objects.get(name=size_name)
            messages.warning(request,f"{size_name} already exists.")
        except Size.DoesNotExist:
            val = Size(name=size_name)
            val.save()
            messages.success(request,f"{size_name} has been added successfully.")
    context = {
        'size' : size
    }
    return render(request,'admin/admin_addsize.html',context)

@login_required(login_url='login')
def admin_viewsize(request):
    size = Size.objects.all()
    context = {
        'size' : size
    }
    return render(request,'admin/admin_viewsize.html',context)

@login_required(login_url='login')
def deletesize(request,id):
    try:
        size = Size.objects.get(id=id)
        size.delete()
        messages.success(request, f"Size {size.name} has been deleted.")
    except Size.DoesNotExist:
        messages.warning(request, "The size you are trying to delete does not exist.")
    return redirect('admin_viewsize')

@login_required(login_url='login')
def admin_editsize(request,id):
    sizes = Size.objects.get(id=id)
    context = {
        'sizes':sizes
    }
    return render(request,'admin/admin_editsize.html',context)

@login_required(login_url='login')
def admin_updatesize(request):
    if request.method == "POST":
        size_id = request.POST.get('size_id')
        size_name = request.POST.get('sizes')
        print("size_name",size_name)
        value = Size.objects.get(id=size_id)
        value.name=size_name
        value.save()
        messages.success(request,f"{size_name} has been updated.")
        return redirect('admin_viewsize')
    return render(request,'admin_viewsize.html')    

@login_required(login_url='login')
def admin_vieworder(request):
    user = request.user.id
    orders = OrderPlaced.objects.all()
    order_list = []
    for order in orders:
        order_dict = {}
        order_dict['order'] = order
        order_dict['product'] = order.product
        order_dict['seller'] = order.product.user.first_name
        order_dict['buyer'] = order.user.first_name
        order_list.append(order_dict)
    context = {
        'order_list':order_list
    }
    return render(request,'admin/admin_vieworder.html',context)        


def adminbase(request):
    return render(request,'admin/adminbase.html')





@login_required(login_url='login')
def admin_deleteproduct(request):
    return render(request,'admin/admin_deleteproduct.html')

@login_required(login_url='login')
def admin_viewallproduct(request):
    product = Product.objects.all()
    context = {
        'product':product
    }
    return render(request,'admin/admin_viewallproduct.html',context)


def admin_viewrequest(request):
    req = Requests.objects.all()
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        status = request.POST.get('status')
        req_obj = Requests.objects.get(id=request_id)
        req_obj.status = status
        req_obj.save()
        return redirect('admin_viewrequest')
    return render(request, 'admin/admin_viewrequest.html', {'req': req})

import calendar
def admin_sellerpayment(request):
    data = Sellerpayment.objects.filter(paid=True,razorpay_payment_status='created',)
    for item in data:
        item.month = calendar.month_name[item.created_at.month]
    print(data)
    return render(request,'admin/admin_sellerpayment.html',{'data':data})





def complaints(request,id):
    user = request.user.id
    order = OrderPlaced.objects.get(id=id)
    product = order.product
    return render(request,'complaint.html',{'product':product})

def feedback(request):
    order = OrderPlaced.objects.all()
    product = Product.objects.all()
    if request.method == 'POST':
        user_id = request.user.id
        message = request.POST.get('msg')
        user = Account.objects.get(id=user_id)
        print("user",user)
        product_id = request.POST.get('product_id')
        print("product_id",product_id)
        product = Product.objects.get(id=product_id)
        print("product",product)
        new_complaint = Query(user=user, product=product, message=message)
        print("new_complaint",new_complaint)
        new_complaint.save()
        messages.success(request, 'Your complaint has been successfully sent!')
        return render(request,'complaint.html')
    else:    
        return render(request,'complaint.html')


#seller complaint

def viewcomplaint(request):
    user = request.user
    comp = Query.objects.filter(product__user=user)
    print("complaint",comp)

    return render(request,'seller/viewcomplaint.html',{'comp':comp})














































# def sellerreg(request):
#     if request.method == "POST":
#         fname = request.POST.get('fname')
#         lname = request.POST.get('lname')
#         address = request.POST.get('addres')
#         brand = request.POST.get('brand')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         city = request.POST.get('city')
#         district = request.POST.get('district')
#         pincode = request.POST.get('pincode')
#         password = request.POST.get('password')
#         cpassword = request.POST.get('cpassword')
#         if password == cpassword:
#             if Seller.objects.filter(email=email).exists():
#                 messages.error(request, 'Email already exists')
#                 return redirect('sellerreg')
#             else:
#                 sell = Seller(first_name=fname,last_name=lname,address=address,brand=brand,email=email,contact=phone,city=city,state=district,pincode=pincode,password=password)
#                 sell.is_staff=True
#                 sell.save()
#                 # messages.info(request, 'Please verify your email for login!')

                       
#             # return redirect('/login/?command=verification&email=' + email)
#         else:
#             print('password is not matching')
#         #     messages.info(request, '!!!Password and Confirm Password are not  match!!!')
#         #     return redirect('sellerreg')
#         #     print('user created')
#     else:
#             # return redirect('login')
#         return render(request, "sellerreg.html")



# def sellerlog(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         pswd = request.POST.get('passwords')
#         print(email, pswd)
#         sell = authenticate(email=email, passwords=pswd)
#         print(sell)

#         if sell is not None:
#             auth.login(request, sell)
#             # save email in session
#             request.session['email'] = email
#             if sell.is_staff:
#                 return redirect('index')
#             # else:
#             #     return redirect('home')
#             # if user.is_staff:
#             #     return redirect('index')
#             else:
#                 return redirect('home')    
#         else:
#             messages.error(request, 'Invalid email or password')
#             return redirect('sellerlog')
#     return render(request, 'sellerlog.html')       