from rest_framework.serializers import ModelSerializer
from .models import User , Branch , City 

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields = ["id" , "username" , "password"]
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
   
class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id" , "number" , "location" ,"city" , "area" , "street" , "manager"]
        
        
        
        
class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ["id" , "city_name"]