'''Database Models'''
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    '''Manager for User models'''

    def create_user(self, mobile, password=None, **extra_fields):
        '''Create save and return a new user'''
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    

    def create_superuser(self, mobile, password):
        '''Create and return a new Super user'''
        user  = self.create_user(mobile, password)
        user.is_staff = True
        user.is_executive = True
        user.is_superuser = True
        user.save()

        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    '''Base user model'''

    name = models.CharField(validators=[RegexValidator(regex='^[a-zA-Z0-9]{6,100}$', message='name should contain atleast 6 letters')])
    mobile = models.CharField(unique=True, validators=[RegexValidator(regex='^[0-9]{10}$', message='mobile number must be 10 digits')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_executive = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'


class Manufacturer(models.Model):
    '''Manufacturer model'''
    name = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name
    

class Brand(models.Model):
    '''Brand model'''
    name = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(default=timezone.now)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name
    

class Category(models.Model):
    '''Category model'''
    name = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    '''Product Model'''
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name


class Variant(models.Model):
    '''Variant Model'''
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    price = models.FloatField()
    SKU = models.CharField(max_length=255, unique=True)
    stock = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name