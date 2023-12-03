from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Account
from django.contrib import auth
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.decorators import login_required
from product.models import Category,Product

from product.models import OrderPlaced,Payment,Cart,Wishlist

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail

# def index(request):
#      return render(request, "index.html")


def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('password')
        print(email, pswd)
        user = auth.authenticate(email=email, password=pswd)
        print(user)

        if user is not None:
            auth.login(request, user)
            # save email in session
            request.session['email'] = email
            if user.is_admin:
                return redirect('admin_dashboard')
            # else:
            #     return redirect('home')
            elif user.approved_staff:
                return redirect('index')
            elif user.approved_delivery:
                return redirect('deliveryorder')    
            elif user.is_user:
                return redirect('home')    
            else:
                messages.warning(request, 'Invalid Credentials')
                return redirect('login')
            # if user.is_staff:
            #     return redirect('index')
            # else:
            #     return redirect('home')    
        else:
            messages.warning(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'login.html')



def register(request):
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
        cpassword = request.POST.get('cpassword')
        roles = request.POST['roles']
        is_user=is_staff=False 
        if roles == 'is_admin':
            is_admin=True
        if roles == 'is_user':
            is_user=True
        else:
            is_staff = True
        if password == cpassword:
            if Account.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists')
                return redirect('register')
            else:
                user = Account.objects.create_user(first_name=fname,last_name=lname,address=address,email=email,contact=phone,city=city,state=district,pincode=pincode,password=password,is_staff=is_staff,is_user=is_user)
                # user.is_user = True
                user.save()
                # messages.info(request, 'Please verify your email for login!')

                current_site = get_current_site(request)
                message = render_to_string('account_verification_email.html', {
                        'user': user,
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })

                send_mail(
                        'Please activate your account',
                        message,
                        'onlinefirststep1@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                messages.warning(request, 'Please verify your email for login !!!')
                return redirect('login')
            # return redirect('/login/?command=verification&email=' + email)
        else:
            print('password is not matching')
            messages.warning(request, '!!!Password and Confirm Password are not  match!!!')
            return redirect('register')
            print('user created')
    else:
            # return redirect('login')
        return render(request, "register.html")

    


# @login_required(login_url='login/')
def logout(request):
    auth.logout(request)
    return redirect('/')


def home(request):
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    count = Cart.objects.filter(user=request.user.id).count()
    category = Category.objects.all()
    products = Product.objects.all()
    # catid = request.GET.get('id')
    # if catid:
    #     products = Product.objects.filter(category_id=catid)
    # else:
    #     products = Product.objects.all()
    return render(request, "home.html", {'data':category,'count':count,'w_count':w_count} )
   


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email


            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'onlinefirststep1@gmail.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.warning(request, 'Account does not exist !!!')
            return redirect('forgotPassword')
    return render(request, 'Forgot_Password.html')




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')    




def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.warning(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')


@login_required(login_url='login')
def account(request):
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    count = Cart.objects.filter(user=request.user.id).count()
    orders = OrderPlaced.objects.filter(
        user=request.user, is_ordered=True).order_by('ordered_date')
    context = {
        'orders': orders,  
        'count':count,
        'w_count':w_count
    }
    return render(request,'account.html',context)


@login_required(login_url='login/')
def changepassword(request):
    count = Cart.objects.filter(user=request.user.id).count()
    w_count = Wishlist.objects.filter(user=request.user.id).count()
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        success = user.check_password(current_password)
        if success:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('login')
        else:
            messages.warning(request, 'Password does not match!')
            return redirect('changepassword')
    return render(request, 'changepassword.html',{'count':count,'w_count':w_count}) 


# def error(request,exception):
#     return render(request, '404.html')

@login_required(login_url='login')
def profile_update(request):
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
        return redirect('account')






# Seller page











































































# 1.------------NORMAL MODEL--------------
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from .models import user_reg,user_log
# from django.shortcuts import redirect
# from hashlib import sha256


# def index(request):
#     return render(request, "index.html")

# def login(request):
#     # if request.method == "POST":
#     #     email=request.POST.get('email')
#     #     password=request.POST.get('password')
#     #     cpwd = request.POST.get('cpassword')
#     #     user=user_reg.objects.filter(email=email,password=cpwd)
#     #     if user:
#     #         user_details=user_reg.objects.get(email=email,password=cpwd)
#     #         email=user_reg.email
#     #         return redirect('index')
#     #     else:
#     #         print("Invalid")          
#     return render(request, 'login.html')




# def register(request):
#     if request.method == "POST":
#         fname = request.POST.get('fname')
#         lname = request.POST.get('lname')
#         address = request.POST.get('addres')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         city = request.POST.get('city')
#         district = request.POST.get('district')
#         pincode = request.POST.get('pincode')
#         password = request.POST.get('password')
#         cpassword = request.POST.get('cpassword')
#         pwd = sha256(cpassword.encode()).hexdigest()
#         if password==cpassword:
#             if user_reg.objects.filter(email=email).exists():
#                 print('email already exists')
#                 return redirect('register')
#             else:
#                 register = user_reg(first_name=fname,last_name=lname,address=address,email=email,contact=phone,city=city,district=district,pincode=pincode,password=pwd)
#                 log = user_log(email=email,password=pwd)
#                 register.save()
#                 log.save()
#                 print("user created")
#                 messages.info(request, 'Your account has been successfully created..!!')
#                 return redirect('login')
#         else:
#              messages.info(request, 'password not matching')
#     return render(request, "register.html")



# def login(request):
#     request.session.flush()
#     if 'email' in request.session:
#         return redirect(home)
#     if request.method=='POST':
#         email = request.POST.get('email')
#         password1 = request.POST.get('password')
#         passw = sha256(password1.encode()).hexdigest()
#         user=user_log.objects.filter(email=email,password=passw)
#         if user:
#             user_details=user_log.objects.get(email=email,password=passw)
#             email=user_details.email
#             request.session['email']=email
#             print("successfully")
#             return redirect('home')
#         else:
#             print("Invalid")
#     return render(request,'login.html')
   



# def forgotpassword(request):
#     return render(request,'forgot-password.html')


# def home(request):
#     if 'email' in request.session:
#         email = request.session['email']
#         return render(request,'home.html',{'email':email})
#     return render(request, "home.html")


# def account(request):
#     return render(request, "account.html")


# # Customer Logout
# def logout(request):
#     if 'email' in request.session:
#         request.session.flush()
#     # auth.logout(request)
#     return redirect(login)     

# def reg(request):
#     return render(request,"reg.html")




















































































































































































# from django.http import HttpResponse
# from django.shortcuts import render
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# import datetime
# # Create your models here.

# class MyAccountManager(BaseUserManager):
#     def create_user(self, first_name=fname,last_name=lname,address=addres,email=email,contact=phone,city=city,state=state,pincode=pincode,is_employee, password=None):
#         if not email:
#             raise ValueError('User must have an email address')

#         if not username:
#             raise ValueError('User must have an username')

#         user = self.model(
#             email = self.normalize_email(email),
#             username = username,
#             first_name = first_name,
#             last_name = last_name,
#             country=country,
#             dob=dob,
#             gender=gender,
#             contact = contact,
#             is_employee=is_employee

#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user


# # class MyAccountManager(BaseUserManager):
# #     def create_user(self,username, email, password=None):
# #         if not email:
# #             raise ValueError('User must have an email address')

# #         if not username:
# #             raise ValueError('User must have an username')

# #         user = self.model(
# #             email = self.normalize_email(email),
# #             username = username,
            
# #         )

# #         user.set_password(password)
# #         user.save(using=self._db)
# #         return user


    
#     def create_superuser(self,username,password,email):
#         user = self.create_user(
#             email = self.normalize_email(email),
#             username = username,
#             password = password,
#             # first_name = first_name,
#             # last_name = last_name,
#         )
#         user.is_admin = True
#         user.is_active = True
#         user.is_staff = True
#         user.is_superadmin = True
#         user.save(using=self._db)
#         return user


 
# class Account(AbstractBaseUser):
    


#     id            = models.AutoField(primary_key=True)
#     first_name      = models.CharField(max_length=50, default='')
#     last_name       = models.CharField(max_length=50, default='')
   
#     username        = models.CharField(max_length=50, unique=True)
#     email           = models.EmailField(max_length=100, unique=True)
#     contact         = models.BigIntegerField(default=0)
#     country          = CountryField(max_length=50,blank_label='(select country)')
#     gender          = models.CharField(max_length=50,choices=gender_choices, default='None')
#     dob             =models.DateField(default=datetime.date.today())



#     # required
#     date_joined     = models.DateTimeField(auto_now_add=True)
#     last_login      = models.DateTimeField(auto_now_add=True)
#     is_admin        = models.BooleanField(default=False)
#     is_company      = models.BooleanField(default=False)
#     is_active       = models.BooleanField(default=True)
#     is_superadmin   = models.BooleanField(default=False)
#     is_employee       = models.BooleanField(default=False)   
#     is_staff        = models.BooleanField(default=False)


#     USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['username', 'first_name', 'last_name','district','state','gender','contact']
#     REQUIRED_FIELDS = ['username','password']




#     objects = MyAccountManager()

#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, add_label):
#         return True




























































# from logapp.models import user_reg
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from django.shortcuts import redirect


# def index(request):
#      return render(request, "index.html")


# def register(request):
#     if request.method == "POST":
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         addres = request.POST['addres']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         city = request.POST['city']
#         state = request.POST['state']
#         pincode = request.POST['pincode']
#         password = request.POST['password']
#         register = user_reg(first_name=fname,last_name=lname,address=addres,email=email,contact=phone,city=city,state=state,pincode=pincode,password=password)
#         register.save()
#         print("user created")
#     return render(request, "register.html")


# def login(request):
#     if request.method == "POST":
#          member = user_reg.objects.all()   
#     return render(request, 'login.html')



#

   







































































# from django.http import HttpResponse
# from django.shortcuts import render
# from django.contrib.auth.models import User
# from .models import Account
# from django.contrib import messages, auth
# from django.shortcuts import redirect
# from django.contrib.auth import authenticate, login, logout

# def index(request):
#      return render(request, "index.html")


# def register(request):
#     if request.method == "POST":
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         addres = request.POST['addres']
#         email = request.POST['email']
#         contact = request.POST['phone']
#         city = request.POST['city']
#         state = request.POST['state']
#         pincode = request.POST['pincode']
#         password = request.POST['password']
#         cpassword= request.POST['cpassword']
#         user = Account.objects.create_user(first_name=fname,last_name=lname,address=addres,email=email,contact=contact,city=city,state=state,pincode=pincode,password=password)
#         user.save()
#         print("user created")
#     return render(request, "register.html")


# def login(request):
#     if request.method == "POST":
#         email = request.POST.get['email']
#         password = request.POST.get['password']
#         user = authenticate(request,email=email, password=password)
#         print(user)
#         if user is not None:
#                 login(request,user)
#                 return redirect('index')
#                 # return render(request, 'index.html')
#         else:
#                 messages.info(request,"Please register")
#                 return redirect('/register')
#     else:
#         return render(request,'login.html')
    


    