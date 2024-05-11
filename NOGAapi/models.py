from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100 , unique=True)
    password = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS=[]
   
class Job_Type(models.Model):
    job_type=models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.job_type
class Employee(models.Model):
    national_number=models.IntegerField(unique=True)
    first_name=models.CharField(max_length=20)
    middle_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=50 , default="test@gmail.com")
    birth_date=models.DateField()
    gender=models.BooleanField()
    salary=models.IntegerField()
    address=models.CharField(max_length=50)
    date_of_employment=models.DateField()
    job_type=models.ForeignKey(Job_Type,on_delete=models.PROTECT,default=1)        
        
# class Employee(models.Model):
#     first_name = models.CharField(max_length=100)
#     middle_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     birth_date = models.DateField()
#     gender = models.BooleanField()
#     salary = models.BooleanField()
#     address = models.CharField(max_length=200)
#     data_of_employment = models.DateField()
    
    
    
class UserEmployee():
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    employee = models.OneToOneField(Employee , on_delete=models.CASCADE)
    
    
class City():
    city_name = models.CharField(max_length=100)
    
class Branch():
    number = models.IntegerField()
    location = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    manager = models.ForeignKey(Employee , on_delete=models.DO_NOTHING)
    # city = models.ForeignKey(City , on_delete=models.DO_NOTHING)
    
    