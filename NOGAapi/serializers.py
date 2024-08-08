from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import Token
from rest_framework.response import Response
import socket
from .models import *
from datetime import datetime
import qrcode
from PIL import Image , ImageDraw
from datetime import date
import io
class Job_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job_Type
        fields=['id','job_type']
  
class EmployeeSerializer(serializers.ModelSerializer):
    job_type_title=serializers.StringRelatedField(source='job_type')
    branch_name = serializers.SerializerMethodField()
    class Meta:
        model=Employee
        fields=['id' , 'national_number','first_name','middle_name','last_name','email','salary','address','date_of_employment','birth_date','gender','job_type' , 'job_type_title' , 'branch' , 'phone' , 'branch_name' , 'image']
        extra_kwargs = {
            "job_type_title" : {'read_only' : True},
            "job_type" : {
                "required":True
            },
            "branch_name" :{
                "read_only" : True
            }
        }
    

    def get_branch_name(self , object):
        if(object.branch):
            return object.branch.city.city_name + " " + str(object.branch.number)
        return 
    
        
        
    def validate(self, attrs):
        request= self.context['request']
        if request.method == 'PUT':
            if self.instance.job_type.job_type == "Manager":
                branches = Branch.objects.all()
                relatedBranches = branches.filter(manager= self.instance.id)
                if(len(relatedBranches) > 0 ):
                    raise serializers.ValidationError({'manager' : ['this employee is a manager to a branche , change the manager on this branch then edit this employee']})
        if request.method in ['POST' , "PUT"]:
            date_of_employment = attrs['date_of_employment']
            birth_date = attrs['birth_date']
            if date_of_employment < birth_date:
                raise serializers.ValidationError({
                    "date_of_employment":"date of employment can't be before the birth date"
                })
            today = date.today()

            eighteen_years_ago = today.replace(year=today.year - 18)

            if birth_date >= eighteen_years_ago:
                raise serializers.ValidationError({
                    "birth_date":"too young"
                })
        return super().validate(attrs)
class UserSerializer(serializers.ModelSerializer):
    # employee=EmployeeSerializer()
    
    class Meta:
        model=User
        fields = ["id" , "username" , "password" , 'employee']
        
        extra_kwargs = {
            "password" : {'write_only' : True},
            'required' : True,
            "id" : {'read_only' : True,
            'required' : True},
            'employee':{'required' : True}
        }
        
    # def validate(self, attrs):
    #     print(self)
        
    #     if(not bool(hasattr(attrs , 'employee'))):        
    #         raise serializers.ValidationError({"error" : 'employee field required'})
    #     return self
    def create(self, validated_data):
        password = validated_data.pop('password' , None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        if(self.user.is_staff):
            data['role'] = 'admin'
        else:
            data['role'] = self.user.employee.job_type.job_type
            if(self.user.employee.branch):
                data['branch'] = self.user.employee.branch.id
                data['branch_name'] = self.user.employee.branch.city.city_name + " " + str(self.user.employee.branch.number) 
                data['image'] = f"{self.context.get('request').build_absolute_uri('/')}media/{str(self.user.employee.image)}" 
        
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
   
class BranchSerializer(serializers.ModelSerializer):
    city_name = serializers.StringRelatedField(source='city')
    manager_name = serializers.StringRelatedField(source='manager')
    class Meta:
        model = Branch
        fields = ["id" , "number" , "location" ,"city" , "area" , "street" , "manager" , "city_name" , 'manager_name']
        extra_kwargs = {
         "city" : {
            "required" : True,
            },
         "manager" : {
            "required" : True,
            },
         "number" : {
             "read_only" : True
             },
         "city_name":{
            "read_only" : True
             } ,
         'manager_name' : {
            "read_only" : True
         }
         }
        
    def create(self, validated_data):
        branches = Branch.objects.filter(city=validated_data['city'])
        branchesOrdered = branches.order_by('number')
        branch = self.Meta.model(**validated_data)
        if len(branchesOrdered)>0:
            maxNumber = branchesOrdered[len(branchesOrdered)-1].number 
            branch.number =  maxNumber +  1
        elif len(branchesOrdered)==0:
            print(len(branchesOrdered))
            
            branch.number =  1
        branch.save()
        manager = Employee.objects.get(id = branch.manager.id)
        manager.branch = branch
        manager.save()

        return branch
    
    def validate(self, attrs):
        if(bool(attrs["manager"].job_type.job_type == "Manager")):
            return super().validate(attrs)
        else:
            raise serializers.ValidationError({"manager" : "employee in not manager"})
        
        
        
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id" , "city_name"]
        
        
        
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['id' , 'national_number','first_name','middle_name','last_name','phone','gender']

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Products_Categories
        fields=['id','category_name']




class PhoneBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Phone_Brand
        fields=['id' , 'brand_name']
        
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields=['id' , 'color']
        
class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model=CPU
        fields=['id' , 'CPU_brand']

class PhoneCamerasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone_Cameras
        fields = ['id' ,'camera_resolution' , 'main']

class PhoneSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(source='brand_id')
    CPU = serializers.StringRelatedField(source='CPU_id')
    color = serializers.StringRelatedField(source='color_id')
    phone_cameras = PhoneCamerasSerializer(many=True)
    class Meta:
        model=Phone
        fields=[ 'CPU_name' , 'RAM' , 'storage' , 'battery' , 'sim' , 'display_size' , 'sd_card' , 'description' , 'release_date' , 'brand_id' , 'CPU_id' , 'color_id' , 'brand' , 'CPU' , 'color' , 'phone_cameras']
        extra_kwargs={
            'brand':{
                'read_only': True,
            },
            'CPU':{
                'read_only': True,
            },
            'color':{
                'read_only': True,
            },
            'brand_id':{
                'required':True
            },
            'CPU_id':{
                'required':True
            },
            'color_id':{
                'required':True
            },
            'phone_cameras':{
                'required' : False
            }
        }
        
   
class AccessoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Accessory_Category
        fields=['id' , 'category_name']
        
class AccessorySerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='accessory_category')
    class Meta:
        model=Accessory
        fields=['description' , 'accessory_category'  , 'category_name']
        extra_kwargs={
            'accessory_category':{
                'required':True
            },
            'category_name':{
                'read_only' : True
            }
        }
class ProductSerializerForSale(serializers.ModelSerializer):
    category_name=serializers.StringRelatedField(
        source='category_type'
    )
    phone = PhoneSerializer()
    accessory = AccessorySerializer()
    class Meta:
        model=Product
        fields=['id','product_name','category_type','category_name' , 'quantity', 'phone' , 'accessory' , 'wholesale_price' , 'selling_price' , 'qr_code' , 'qr_codes_download']
        extra_kwargs={
            'category_name' : {
                'read_only' : True,
            },
            'category_type' : {
                'required' : True
            }
        }
# def genereate_employee_card(image_url , n):
    
def genereate(image_url , product):
    A4 = Image.open(f'mediafiles/productqr/A4.jpg')
    img = Image.open(image_url)
    new_image = Image.new('RGB',(A4.width,A4.height), (250,250,250))
    number_of_rows = A4.height//img.height
    number_of_cols = A4.width//img.width

    for j in range(0 , number_of_rows): 
        for i in range(0,number_of_cols):
            draw = ImageDraw.Draw(img)
            new_image.paste(img , (img.width*i,img.height*j))
    draw = ImageDraw.Draw(new_image)
    draw.text((10, A4.height-20), "NOGA project 2024" , fill='Black' )
    draw.text((300, A4.height-20), product , fill='Black' )
    return new_image
               
class ProductSerializer(serializers.ModelSerializer):
    category_name=serializers.StringRelatedField(
        source='category_type'
    )
    phone = PhoneSerializer()
    accessory = AccessorySerializer()
    class Meta:
        model=Product
        fields=['id' , 'product_name','wholesale_price','selling_price','quantity','category_type','category_name' , 'phone' , 'accessory' ,'qr_code' , 'qr_codes_download']
        extra_kwargs={
            'category_name' : {
                'read_only' : True,
            },
            'category_type' : {
                'required' : True
            }
        }
    def __init__(self ,  *args, **kwargs ):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']
        if request.method in ["POST" , "PUT"]:
            if 'category_type' in self.initial_data:
                category_type = self.initial_data.get('category_type')
                
                if category_type == 1:
                    self.fields['accessory'].required = False
                    self.fields['phone'].required = True
                elif category_type == 2:
                    self.fields['phone'].required = False
                    self.fields['accessory'].required = True
        # elif request.method in ["GET"]:
        #     category_type = request.data['category_type']
        #     if category_type == 1:
        #         self.fields['phone'].read_only = False
        #     elif category_type == 2:
        #         self.fields['phone'].read_only = False
                       
                
    def create(self, validated_data):
       
        if validated_data['category_type'].category_name == "Phone":
            phone_data = validated_data.pop('phone')
            phone_cameras_data = phone_data.pop('phone_cameras' , None)
            product_instance = Product.objects.create(**validated_data)
            phone_instance = Phone.objects.create(product=product_instance,**phone_data)
            file_name = f"product-{product_instance.id}.png"
            download_file_name = f"product-{product_instance.id}-download.jpg"
            path = f'mediafiles/productqr'
            file_path = f"{path}/{file_name}"
            download_file_path = f"{path}/{download_file_name}"
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=3)
            qr.add_data(f"product-{product_instance.id}")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save(file_path, 'PNG')
            download_image = genereate(file_path , f"{product_instance.product_name}")
            download_image.save(download_file_path)
            product_instance.qr_code = f"{self.context.get('request').build_absolute_uri('/')}media/productqr/{file_name}"
            product_instance.qr_codes_download = f"{self.context.get('request').build_absolute_uri('/')}media/productqr/{download_file_name}"
            product_instance.save()
            
            if phone_cameras_data:
                for phone_camera_data in phone_cameras_data:
                    phone_camera_instanse = Phone_Cameras.objects.create(product = phone_instance , **phone_camera_data)
                    phone_camera_instanse.save()
            phone_instance.save()
                
            print(product_instance.qr_codes_download)
            return product_instance
        
        if validated_data['category_type'].category_name == "Accessory":
            accessory_data = validated_data.pop('accessory')
            product_instance = Product.objects.create(**validated_data)
            file_name = f"product-{product_instance.id}.png"
            download_file_name = f"product-{product_instance.id}-download.jpg"
            path = f'mediafiles/productqr'
            file_path = f"{path}/{file_name}"
            download_file_path = f"{path}/{download_file_name}"
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=3)
            qr.add_data(f"product-{product_instance.id}")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save(file_path, 'PNG')
            download_image = genereate(file_path , f"{product_instance.product_name}")
            download_image.save(download_file_path)
            product_instance.qr_code = f"{self.context.get('request').build_absolute_uri('/')}media/productqr/{file_name}"
            product_instance.qr_codes_download = f"{self.context.get('request').build_absolute_uri('/')}media/productqr/{download_file_name}"
            product_instance.save()
            accessory_instance = Accessory.objects.create(product=product_instance,**accessory_data)
            accessory_instance.save()
            
            return product_instance
        
    def update(self, instance, validated_data):
        #update the product
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.wholesale_price = validated_data.get('wholesale_price', instance.wholesale_price)
        instance.selling_price = validated_data.get('selling_price', instance.selling_price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.category_type = validated_data.get('category_type', instance.category_type)
        
        
        if validated_data['category_type'].category_name == "Phone":
            phone_data = validated_data.pop('phone')
            phone_cameras_data = phone_data.pop('phone_cameras')
            #update phone and create if it dosen't exist
            try:
                phone_instance = Phone.objects.get(product=instance)
                phone_instance.CPU_name = phone_data.get('CPU_name' , phone_instance.CPU_name)
                phone_instance.RAM = phone_data.get('RAM' , phone_instance.RAM)
                phone_instance.storage = phone_data.get('storage' , phone_instance.storage)
                phone_instance.battery = phone_data.get('battery' , phone_instance.battery)
                phone_instance.sim = phone_data.get('sim' , phone_instance.sim)
                phone_instance.display_size = phone_data.get('display_size' , phone_instance.display_size)
                phone_instance.sd_card = phone_data.get('sd_card' , phone_instance.sd_card)
                phone_instance.description = phone_data.get('description' , phone_instance.description)
                phone_instance.release_date = phone_data.get('release_date' , phone_instance.release_date)
                phone_instance.brand_id = phone_data.get('brand_id' , phone_instance.brand_id)
                phone_instance.CPU_id = phone_data.get('CPU_id' , phone_instance.CPU_id)
                phone_instance.color_id = phone_data.get('color_id' , phone_instance.color_id)
                phone_instance.save()
                
                this_phone_cameras= Phone_Cameras.objects.filter(product = phone_instance)
                if(len(this_phone_cameras) != 0):
                    print(len(this_phone_cameras))
                    for phone_camera_instance in this_phone_cameras:
                        phone_camera_instance.delete()
                for phone_camera_data in phone_cameras_data:
                    phone_camera_instanse = Phone_Cameras.objects.create(product = phone_instance , **phone_camera_data)
                
                # for phone_camera_data in phone_cameras_data:
                #     try:
                #         phone_camera_instance = Phone_Cameras.objects.get(product=phone_instance)
                #         phone_camera_instance.camera_resolution = phone_camera_data.get('camera_resolution' , phone_camera_instance.camera_resolution)
                #         phone_camera_instance.main = phone_camera_data.get('main' , phone_camera_instance.main)
                #         phone_camera_instance.save()
                        
                        
                    # except Phone_Cameras.DoesNotExist:
            except Phone.DoesNotExist:
                phone_instance = Phone.objects.create(product=instance,**phone_data)
                for phone_camera_data in phone_cameras_data:
                    phone_camera_instanse = Phone_Cameras.objects.create(product = phone_instance , **phone_camera_data)
                
            #delete if there is unwanted accessory
                
            try:
                accessory_instance = Accessory.objects.get(product=instance )
                accessory_instance.delete()
            except Accessory.DoesNotExist:
                print("123123")
            return instance
        
        if validated_data['category_type'].category_name == "Accessory":
            accessory_data = validated_data.pop('accessory')
            #update accessory and create if it dosen't exist
            
            try:
                accessory_instance = Accessory.objects.get(product=instance)
                accessory_instance.description = accessory_data.get('description' , accessory_instance.description)
                accessory_instance.accessory_category = accessory_data.get('accessory_category' , accessory_instance.accessory_category)
                accessory_instance.save()
                
            except Accessory.DoesNotExist:
                accessory_instance = Accessory.objects.create(product=instance,**accessory_data)
                
            #delete if there is unwanted phone
            try:
                phone_instance = Phone.objects.get(product=instance )
                phone_instance.delete()
            except Phone.DoesNotExist:
                print("123123")
            return instance
    
    
    
class EnteredProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entered_Product
        fields=['process' , 'product' , 'quantity' , 'wholesale_price' , 'selling_price']
        extra_kwargs = {
            "process":{
                "read_only" : True,
            },
             "wholesale_price":{
                "required" : False,
            },
              "selling_price":{
                "required" : False,
            },
            
        }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product = ProductSerializerForSale(instance.product)
        representation['product'] = product.data
        return representation
        
    
            
class EntryProcessSerializer(serializers.ModelSerializer):
    entered_products = EnteredProductSerializer(many=True )
    class Meta:
        model = Entry_process
        fields = ['id' , 'date_of_process' , 'entered_products' ]
        extra_kwargs = {
            "date_of_process":{
                "read_only" : True
            },
            
        }
    
    def create(self, validated_data):
        entered_products_data = validated_data.pop('entered_products')
        # date_of_process = datetime.today().strftime('%Y-%m-%d')
        # validated_data['date_of_process'] = date_of_process
        entry_process_instance = Entry_process.objects.create(**validated_data)
        entry_process_instance.save()
        for entered_product_data in entered_products_data:
            # product_instance = Product.objects.get(id=entered_product_data['product'])
            product_instance = entered_product_data['product']
            product_instance.quantity +=  entered_product_data.get('quantity' , 0)
            product_instance.wholesale_price =  entered_product_data.get('wholesale_price' , product_instance.wholesale_price)
            product_instance.selling_price =  entered_product_data.get('selling_price' , product_instance.selling_price)
            if('wholesale_price' in entered_product_data):
                print('there is wholesale_price')
            else:
                print('there is no wholesale_price')
                entered_product_data['wholesale_price'] = product_instance.wholesale_price
                
            if('selling_price' in entered_product_data):
                print('there is selling_price')
            else:
                print('there is no selling_price')
                entered_product_data['selling_price'] = product_instance.selling_price
            entered_product_instance = Entered_Product.objects.create(process = entry_process_instance , **entered_product_data)
                
            product_instance.save()
            entered_product_instance.save()
        return entry_process_instance

class TransportedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transported_Product
        fields = ['product' , 'wholesale_price', 'selling_price', 'quantity']
        extra_kwargs = {
            "process":{
                    "read_only" : True,
                },
            "wholesale_price":{
                    "read_only" : True,
            },
            "selling_price":{
                    "read_only" : True,
            }
        }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product = ProductSerializerForSale(instance.product)
        representation['product'] = product.data
        return representation
        
class ProductsMovmentSerializer(serializers.ModelSerializer):
    # transported_products = TransportedProductsSerializer(many=True)
    transported_product = TransportedProductsSerializer(many=True)
    branch_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    class Meta:
        model = Products_Movment
        fields = ['id' , 'branch' , 'branch_name' , 'address'  , 'date_of_process' , 'movement_type' , 'transported_product' ]
        extra_kwargs = {
            "date_of_process":{
                "read_only" : True
            },

        }
    def get_branch_name(self , object):
        if(object.branch):
            return object.branch.city.city_name + " " + str(object.branch.number)
        return 
    def get_address(self , object):
        if(object.branch):
            return object.branch.street + ' , ' +  object.branch.area + ' , ' + object.branch.city.city_name
        return 
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        transported_products_data = validated_data['transported_product']
        movement_type = validated_data['movement_type']
        error = {
            "transported_product":[
                
            ]
        }
        products = []
        if movement_type:
            
            for index , transported_product_data in enumerate(transported_products_data):
                if(transported_product_data['product'].id in products):
                    error['transported_product'].append({"product":f" repeated product in the {index+1}th product "})
                products.append(transported_product_data['product'].id)
                product_instance = Product.objects.get(id=transported_product_data['product'].id)
                if transported_product_data['quantity'] > product_instance.quantity:
                    error['transported_product'].append({"quantity":f"we don't have that much in the main warehouse for the {index+1}th product , we only have {product_instance.quantity}"})
                    
                        
            
        else:
            for index , transported_product_data in enumerate(transported_products_data):
                if(transported_product_data['product'] in products):
                    error['transported_product'].append({"product":f" repeated product in the {index+1}th product "})
                products.append(transported_product_data['product'].id)
                try:
                    product_instance = Branch_Products.objects.get(product=transported_product_data['product'] , branch = validated_data['branch'])
                    if transported_product_data['quantity'] > product_instance.quantity:
                        error['transported_product'].append({"quantity":f"we don't have that much in the branch warehouse for the {index+1}th product , we only have {product_instance.quantity} "})
                except Branch_Products.DoesNotExist:
                    error['transported_product'].append({"product":f"we don't have that product in this branch warehouse for the {index+1}th product  "})
                    
        if len(error['transported_product']) > 0:
            raise serializers.ValidationError(error)
        else:
            return validated_data
                

    def create(self, validated_data):
        print(validated_data)
        transporterd_products_data = validated_data.pop('transported_product')
        print(validated_data)
        
        # date_of_process = datetime.today().strftime('%Y-%m-%d')
        # validated_data['date_of_process'] = date_of_process
        products_movment_instance = Products_Movment.objects.create(**validated_data)
        for transported_product_data in transporterd_products_data:
            product_instance = Product.objects.get(id=transported_product_data['product'].id)
            transported_product_data['wholesale_price'] = product_instance.wholesale_price
            transported_product_data['selling_price'] = product_instance.selling_price
            transported_product_instance = Transported_Product.objects.create(process = products_movment_instance , **transported_product_data)
            
            try:
                branch_product_instance = Branch_Products.objects.get(product=transported_product_instance.product , branch = products_movment_instance.branch)
                
                if products_movment_instance.movement_type:
                    branch_product_instance.quantity += transported_product_instance.quantity
                    product_instance.quantity -= transported_product_instance.quantity
                    
                else:
                    branch_product_instance.quantity -= transported_product_instance.quantity
                    product_instance.quantity += transported_product_instance.quantity
                    
                product_instance.save()
                branch_product_instance.save()
                
            except Branch_Products.DoesNotExist:
                branch_product_instance = Branch_Products.objects.create(product=transported_product_instance.product , branch = products_movment_instance.branch , quantity = transported_product_instance.quantity)
                product_instance = Product.objects.get(id=transported_product_data['product'].id)
                
                if products_movment_instance.movement_type:
                    product_instance.quantity -= transported_product_instance.quantity
                    
                else:
                    product_instance.quantity += transported_product_instance.quantity
                    
                product_instance.save()
                branch_product_instance.save()
            transported_product_instance.save()
        products_movment_instance.save()
        return products_movment_instance
    
class BranchProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializerForSale()
    branch_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    class Meta:
        model = Branch_Products
        fields = ['branch' , 'branch_name' , 'address' , 'product' , 'quantity']
        unique_together = ['branch', 'product']
    def get_branch_name(self , object):
        if(object.branch):
            return object.branch.city.city_name + " " + str(object.branch.number)
        return 
    def get_address(self , object):
        if(object.branch):
            return object.branch.street + ' , ' +  object.branch.area + ' , ' + object.branch.city.city_name
        return     
class BranchProductsForSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch_Products
        fields = [ 'product' , 'quantity']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product = ProductSerializerForSale(instance.product)
        representation['product'] = product.data
        return representation
    
#---new---
class RequestedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Requested_Products
        fields=['id' , 'product_id','quantity','status']
        extra_kwargs = {
            "status":{
                "read_only":True
            }
        }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product = ProductSerializerForSale(instance.product_id)
        representation['product'] = product.data
        return representation
  

class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Request_Status
        fields='__all__'
        
class BranchesRequestsSerializer(serializers.ModelSerializer):
    requests=RequestedProductsSerializer(many=True)
    class Meta:
        model=Branches_Requests
        fields=['id','branch_id','date_of_request','note','requests']
  
    def create(self, validated_data):
        RequestedProducts=validated_data.pop('requests')
        branch=Branches_Requests.objects.create(**validated_data)
        request_status_pending = Request_Status.objects.get(id=1) 
        
        for req_product in RequestedProducts:
            req_product['status'] = request_status_pending
            Requested_Products.objects.create(request_id=branch,**req_product)
            

        return branch


class PurchasedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Purchased_Products
        fields=['product_id','wholesale_price','selling_price','purchased_quantity']
        extra_kwargs = {
            "wholesale_price":{
                "read_only":True
            },
            "selling_price":{
                "read_only":True
            }
            
        }
class PurchaseSerializer(serializers.ModelSerializer):
    
    products=PurchasedProductsSerializer(many=True)
    branch_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()



    class Meta:
        model=Purchase
        fields=['purchase_id','branch_id' , 'branch_name' , 'address','date_of_purchase','customer_id','products']
        
    def get_branch_name(self , object):
        if(object.branch_id):
            return object.branch_id.city.city_name + " " + str(object.branch_id.number)
        return 
    def get_address(self , object):
        if(object.branch_id):
            return object.branch_id.street + ' , ' +  object.branch_id.area + ' , ' + object.branch_id.city.city_name
        return     
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        products_data = validated_data['products']
        error = {
            "purchaced_products":[
                
            ]
        }
        products = []
         
        for index , product_data in enumerate(products_data):
            if(product_data['product_id'] in products):
                error['purchaced_products'].append({"product":f" repeated product in the {index+1}th product "})

            products.append(product_data['product_id'])
            try:
                product_instance = Branch_Products.objects.get(product=product_data['product_id'] , branch = validated_data['branch_id'])
                if product_data['purchased_quantity'] > product_instance.quantity:
                    error['purchaced_products'].append({"quantity":f"we don't have that much in the branch warehouse for the {index+1}th product , we only have {product_instance.quantity} "})
            except Branch_Products.DoesNotExist:
                product_in_other_branches = Branch_Products.objects.filter(product=product_data['product_id'])
                product_in_other_branches_serialized = BranchProductsSerializer(many=True , data=product_in_other_branches)
                product_in_other_branches_serialized.is_valid()
                error['purchaced_products'].append({
                    "product":f"we don't have that product in this branch warehouse for the {index+1}th product ",
                    "other_options":product_in_other_branches_serialized.data
                    })
                
        if len(error['purchaced_products']) > 0:
            raise serializers.ValidationError(error)
        else:
            return validated_data
                

    
    def __init__(self,*args,**kwargs):
        super(PurchaseSerializer,self).__init__(*args, **kwargs)
        request=kwargs['context']['request']
        if request.method in ["POST","PUT"]:
            if 'products' in self.initial_data:
                purchased_products = self.initial_data['products']
                thereIsPhone = False
                for purchace_product in purchased_products:
                    product_instance = Product.objects.get(id=purchace_product['product_id'])
                    if product_instance.category_type.category_name == 'Phone':
                        thereIsPhone=True
                        break
                if thereIsPhone==True:
                    self.fields['customer_id'].required=True
                    
    def create(self, validated_data):
        purchased_products=validated_data.pop('products')
        purchase=Purchase.objects.create(**validated_data)
        for product in purchased_products:
            product_instance = Branch_Products.objects.get(product=product['product_id'] , branch = validated_data['branch_id'])
            main_product_instance = Product.objects.get(id=product['product_id'].id)
            product_instance.quantity -= product['purchased_quantity']
            product['wholesale_price'] = main_product_instance.wholesale_price
            product['selling_price'] = main_product_instance.selling_price
            product_instance.save()
            Purchased_Products.objects.create(purchase_id=purchase,**product)
            

        return purchase
    