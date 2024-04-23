from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields = ["id" , "username" , "password"]
        extra_kwargs = {
            "password" : {'write_only' : True},
            "id" : {'write_only' : True},
        }
        
        
    def create(self, validated_data):
        password = validated_data.pop('password' , None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
   
        