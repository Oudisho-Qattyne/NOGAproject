from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import Token
from .models import *

class Job_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job_Type
        fields=['id','job_type']
  
class EmployeeSerializer(serializers.ModelSerializer):
    job_type_title=serializers.StringRelatedField(source='job_type')
    branch_name = serializers.SerializerMethodField()
    class Meta:
        model=Employee
        fields=['id' , 'national_number','first_name','middle_name','last_name','email','salary','address','date_of_employment','birth_date','gender','job_type' , 'job_type_title' , 'branch' , 'phone' , 'branch_name']
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
        fields=['national_number','first_name','middle_name','last_name','phone','gender']

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
        
class PhoneSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(source='brand_id')
    CPU = serializers.StringRelatedField(source='CPU_id')
    color = serializers.StringRelatedField(source='color_id')
    class Meta:
        model=Phone
        fields=[ 'CPU_name' , 'RAM' , 'storage' , 'battery' , 'sim' , 'display_size' , 'sd_card' , 'description' , 'release_date' , 'brand_id' , 'CPU_id' , 'color_id' , 'brand' , 'CPU' , 'color']
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
        
        
class ProductSerializer(serializers.ModelSerializer):
    category_name=serializers.StringRelatedField(
        source='category_type'
    )
    phone = PhoneSerializer()
    accessory = AccessorySerializer()
    class Meta:
        model=Product
        fields=['id' , 'product_name','wholesale_price','selling_price','quantity','category_type','category_name' , 'phone' , 'accessory']
        extra_kwargs={
            'category_name' : {
                'read_only' : True,
            },
            'category_type' : {
                'required' : True
            }
        }