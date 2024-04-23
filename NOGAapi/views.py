from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
# Create your views here.


class RrgisterAPIView(APIView):
    def post(self , requset):
        data = requset.data
        if(data["password"] != data["confirm_password"]):
            return Response({
                "validationError" : "password and confirm_password don't macth",
            })
        serializedData = UserSerializer(data=requset.data)
        serializedData.is_valid(raise_exception=True)
        serializedData.save()
        
        return Response(serializedData.data , status=status.HTTP_200_OK)