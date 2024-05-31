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
    class Meta:
        model=Employee
        fields=['id' , 'national_number','first_name','middle_name','last_name','email','salary','address','date_of_employment','birth_date','gender','job_type' , 'job_type_title']
        extra_kwargs = {
            "job_type_title" : {'read_only' : True},
            "job_type" : {'write_only' : True,
                          "required":True
                          },
        }


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
        
        data['role'] = self.user.employee.job_type.job_type
        
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
   
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id" , "number" , "location" ,"city" , "area" , "street" , "manager"]
        extra_kwargs = {
         "city" : {"required" : True},
         "manager" : {"required" : True}
         }
    def validate(self, attrs):
        if(bool(attrs["manager"].job_type.job_type == "Manager")):
            return super().validate(attrs)
        else:
            raise serializers.ValidationError({"manager" : "employee in not manager"})
        
        
        
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id" , "city_name"]