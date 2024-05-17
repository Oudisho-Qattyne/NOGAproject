from rest_framework import serializers
from .models import *

class Job_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job_Type
        fields=['id','job_type']


class EmployeeSerializer(serializers.ModelSerializer):
    job_type=Job_TypeSerializer()
    class Meta:
        model=Employee
        fields=['national_number','first_name','middle_name','last_name','email','salary','address','date_of_employment','birth_date','gender','job_type']
        


class UserSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    
    class Meta:
        model=User
        fields = ["id" , "username" , "password" , 'employee']
        extra_kwargs = {
            "password" : {'write_only' : True},
            "id" : {'read_only' : True},
        }
        
        
    def create(self, validated_data):
        password = validated_data.pop('password' , None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
   
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id" , "number" , "location" ,"city" , "area" , "street" , "manager"]
        
        
        
        
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id" , "city_name"]