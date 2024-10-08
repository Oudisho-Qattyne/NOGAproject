from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers

# Create your models here.

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB in bytes

# Validate the size of uploaded images
def validate_image_size(value):
    if value.size > MAX_IMAGE_SIZE:
        raise serializers.ValidationError("Image file size is too large (max 2MB)")



class City(models.Model):
    def __str__(self) -> str:
        return self.city_name
    city_name = models.CharField(max_length=100 , unique=True)
    
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
    def __str__(self) -> str:
        return self.first_name + " " + self.middle_name + " " + self.last_name
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
    branch = models.ForeignKey(Branch ,on_delete=models.SET_NULL , null=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True , validators=[validate_image_size])

class User(AbstractUser):
    username = models.CharField(max_length=100 , unique=True)
    password = models.CharField(max_length=100)
    employee = models.OneToOneField(Employee , on_delete=models.CASCADE , null=True)
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
    
class User_Employee(models.Model):
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
    def __str__(self) -> str:
        return self.product_name
    product_name=models.CharField(max_length=100)
    wholesale_price=models.IntegerField()
    selling_price=models.IntegerField()
    quantity=models.PositiveIntegerField()
    category_type=models.ForeignKey(Products_Categories,on_delete=models.PROTECT,default=1)
    qr_code = models.CharField(max_length=300 , null=True)
    qr_codes_download = models.CharField(max_length=300 , null=True)


#----new----
class Phone_Brand(models.Model):
    def __str__(self) -> str:
        return self.brand_name
    # brand_id=models.IntegerField(primary_key=True)
    brand_name=models.CharField(max_length=20 , unique=True)

class Color(models.Model):
    def __str__(self) -> str:
        return self.color
    # color_id=models.IntegerField(primary_key=True)
    color=models.CharField(max_length=20 , unique=True)

class CPU(models.Model):
    def __str__(self) -> str:
        return self.CPU_brand
    # CPU_id=models.IntegerField(primary_key=True)
    CPU_brand=models.CharField(max_length=50 , unique=True)


class Phone(models.Model):
    
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    CPU_name=models.CharField(max_length=50)
    RAM=models.IntegerField()
    storage=models.IntegerField()
    battery=models.IntegerField()
    sim=models.IntegerField()
    display_size=models.FloatField()
    sd_card=models.BooleanField()
    description=models.CharField(max_length=200)
    release_date=models.DateField()
    brand_id=models.ForeignKey(Phone_Brand,on_delete=models.CASCADE)
    CPU_id=models.ForeignKey(CPU,on_delete=models.CASCADE)
    color_id=models.ForeignKey(Color,on_delete=models.CASCADE)
    
    @property
    def phone_cameras(self):
        return self.phone_cameras_set.all()

class Phone_Cameras(models.Model):
    product=models.ForeignKey(Phone,on_delete=models.CASCADE)
    camera_resolution=models.FloatField()
    main=models.BooleanField()

class Accessory_Category(models.Model):
    def __str__(self):
        return self.category_name
    # accessory_category=models.IntegerField(primary_key=True)
    category_name=models.CharField(max_length=20 , unique=True)
 
class Accessory(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    accessory_category=models.ForeignKey(Accessory_Category,on_delete=models.CASCADE)


class Phones_Accessories(models.Model):
    phone=models.ForeignKey(Phone,on_delete=models.CASCADE)
    accessor=models.ForeignKey(Accessory,on_delete=models.CASCADE)
    
    
class Entry_process(models.Model):
    date_of_process = models.DateField(auto_now_add=True)
    
    @property
    def entered_products(self):
        return self.entered_product_set.all()
    
class Entered_Product(models.Model):
    process = models.ForeignKey(Entry_process , on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    wholesale_price=models.IntegerField(null=True)
    selling_price=models.IntegerField(null=True)
    
class Branch_Products(models.Model):
    branch = models.ForeignKey(Branch , on_delete=models.PROTECT)
    product = models.ForeignKey(Product , on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    
    
class Products_Movment(models.Model):
    branch = models.ForeignKey(Branch , on_delete=models.PROTECT)
    date_of_process = models.DateField(auto_now_add=True)
    movement_type = models.BooleanField()
    
    @property
    def transported_product(self):
        return self.transported_product_set.all()
    
class Transported_Product(models.Model):
    process = models.ForeignKey(Products_Movment , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.PROTECT)
    wholesale_price  = models.IntegerField()
    selling_price = models.IntegerField()
    quantity = models.PositiveIntegerField()
    
    
#------Request----   
class Branches_Requests(models.Model):
    @property
    def requests(self):
         return self.requested_products_set.all()
    branch_id=models.ForeignKey(Branch,on_delete=models.CASCADE)
    date_of_request=models.DateField(auto_now_add=True)
    note=models.CharField(max_length=150 , null=True)
    processed = models.BooleanField(default=False)

class Request_Status(models.Model):
    status=models.CharField(max_length=100)

class Requested_Products(models.Model):
    request_id=models.ForeignKey(Branches_Requests,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    status=models.ForeignKey(Request_Status,on_delete=models.CASCADE)

#------Purchase----
class Purchase(models.Model):
    @property
    def products(self):
         return self.purchased_products_set.all()
    purchase_id=models.BigAutoField(primary_key=True,auto_created=True)
    branch_id=models.ForeignKey(Branch,on_delete=models.PROTECT)
    customer_id=models.ForeignKey(Customer,null=True,on_delete=models.PROTECT)
    date_of_purchase=models.DateField(auto_now_add=True)


class Purchased_Products(models.Model):
    purchase_id=models.ForeignKey(Purchase,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.PROTECT)
    wholesale_price=models.IntegerField()
    selling_price=models.IntegerField()
    purchased_quantity=models.PositiveIntegerField()
