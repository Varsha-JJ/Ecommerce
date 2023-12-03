from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.contrib.auth.models import User

class MyAccount(BaseUserManager):
    def create_user(self, first_name, last_name, address, email, contact, city, state, pincode,is_staff,is_user,password=None):
        if not email:
            raise ValueError('User must have an email address')

    

        user = self.model(
            email = self.normalize_email(email),
            # username = username,
            first_name = first_name,
            last_name = last_name,
            address = address,
            contact = contact,
            city = city,
            state = state,
            pincode = pincode,
            is_user = is_user,
            is_staff = is_staff,
            
           
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self,password,email,**extra_feilds):
        user = self.create_user(
            email = self.normalize_email(email),
            # username = username,
            **extra_feilds,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

role_choices = (('customer','customer'),('seller','seller'),('None','None'))
 
class Account(AbstractBaseUser, PermissionsMixin):
    id              = models.AutoField(primary_key=True)
    first_name      = models.CharField(max_length=50, default='')
    last_name       = models.CharField(max_length=50, default='') 
    address         = models.CharField(max_length=100) 
    email           = models.CharField(max_length=200,unique=True)
    contact         = models.BigIntegerField(default=0)
    city            = models.CharField(max_length=50, default='')
    state           = models.CharField(max_length=50, default='')
    pincode         = models.BigIntegerField(default=0)
    password        = models.CharField(max_length=200)
    roles           = models.CharField(max_length=100,choices=role_choices,default="")


    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_user         = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    approved_staff  = models.BooleanField(default=False)
    approved_delivery = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','address','contact','city','state','pincode','password','is_staff','is_user']
    # REQUIRED_FIELDS = ['password']




    objects = MyAccount()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    @staticmethod
    def get_active_staff_users():
        return Account.objects.filter(is_staff=True, is_active=True,is_superuser=False,approved_delivery=False,approved_staff=True)
    
    def get_active_users():
        return Account.objects.filter(is_user=True, is_active=True,approved_delivery=False)
    
    @staticmethod
    def active_users_with_staff_role():
        return Account.objects.filter(is_active=True, is_user=True, is_staff=True)
    # def get_active_staff_users(self):
    #     return self.filter(is_active=True, is_staff=True, is_superuser=False, is_superadmin=False)    


# class Seller(models.Model):
#     id              = models.AutoField(primary_key=True)
#     first_name      = models.CharField(max_length=50, default='')
#     last_name       = models.CharField(max_length=50, default='') 
#     address         = models.CharField(max_length=100) 
#     brand           = models.CharField(max_length=100)
#     email           = models.CharField(max_length=200,unique=True)
#     contact         = models.BigIntegerField(default=0)
#     city            = models.CharField(max_length=50, default='')
#     state           = models.CharField(max_length=50, default='')
#     pincode         = models.BigIntegerField(default=0)
#     password        = models.CharField(max_length=200)

#     # required
#     date_joined     = models.DateTimeField(auto_now_add=True)
#     last_login      = models.DateTimeField(auto_now_add=True)
#     is_active       = models.BooleanField(default=False)
#     is_staff        = models.BooleanField(default=False)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name','address','brand','contact','city','state','pincode','password']
#     is_seller       = models.BooleanField(default=False)
#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'

#     def __str__(self):
#         return self.email


    















































# class user_reg(models.Model):


#     first_name      = models.CharField(max_length=50, default='')
#     last_name       = models.CharField(max_length=50, default='') 
#     address         = models.CharField(max_length=100) 
#     email           = models.CharField(max_length=200,unique=True)
#     contact         = models.BigIntegerField(default=0)
#     city            = models.CharField(max_length=50, default='')
#     district        = models.CharField(max_length=50, default='')
#     pincode         = models.BigIntegerField(default=0)
#     password        = models.CharField(max_length=200)


#     def __str__(self):
#          return self.email


# #Login Table
# class user_log(models.Model):
#      email    = models.CharField(max_length=200,primary_key=True,unique=True)
#      password = models.CharField(max_length=200)











































































































































