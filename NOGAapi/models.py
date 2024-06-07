from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class City(models.Model):
    city_name = models.CharField(max_length=100)
    
class Branch(models.Model):
    number = models.IntegerField()
    location = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    manager = models.OneToOneField("Employee" , on_delete=models.PROTECT , related_name='manager_of_branch')
    city = models.ForeignKey(City , on_delete=models.PROTECT )
    
class Job_Type(models.Model):
    job_type=models.CharField(max_length=100 , unique=True)
    def __str__(self) -> str:
        return self.job_type
        
class Employee(models.Model):
    national_number=models.IntegerField(unique=True)
    first_name=models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=50 , default="test@gmail.com")
    birth_date=models.DateField()
    gender=models.BooleanField()
    salary=models.IntegerField()
    address=models.CharField(max_length=50)
    phone=models.CharField(max_length=100)
    date_of_employment=models.DateField()
    job_type=models.ForeignKey(Job_Type,on_delete=models.PROTECT,default=1)        
    branch = models.ForeignKey(Branch ,on_delete=models.PROTECT , null=True)

class User(AbstractUser):
    username = models.CharField(max_length=100 , unique=True)
    password = models.CharField(max_length=100)
    employee = models.OneToOneField(Employee , on_delete=models.PROTECT , null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS=[]
    def __str__(self) -> str:
        return self.username
    
#     {
# "username":"Oudisho Qattyne",
# "password":"qqqqqqqq",
# "confirm_password":"qqqqqqqq",
# "employee":1
# }
    
class UserEmployee(models.Model):
    user = models.OneToOneField(User , on_delete=models.PROTECT)
    employee = models.OneToOneField(Employee , on_delete=models.PROTECT)
    
class Customer(models.Model):
    national_number=models.IntegerField(unique=True)
    first_name=models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=13)
    gender=models.BooleanField()


class Products_Categories(models.Model):
    category_name=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.category_name

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    wholesale_price=models.IntegerField()
    selling_price=models.IntegerField()
    quantity=models.IntegerField()
    category_type=models.ForeignKey(Products_Categories,on_delete=models.PROTECT,default=1)




    