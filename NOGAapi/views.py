from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import UserSerializer
from django_filters import rest_framework as filter
from rest_framework import filters
from .models import User
# Create your views here.
# --------Employees---------

class Job_TypeView(generics.ListAPIView,generics.ListCreateAPIView):
    queryset=Job_Type.objects.all()
    serializer_class=Job_TypeSerializer
    filter_backends=[filter.DjangoFilterBackend]
    filterset_fields=['id','job_type']

class EmployeesApiView(generics.ListAPIView,generics.ListCreateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    filter_backends=[filter.DjangoFilterBackend]
    filterset_fields=['national_number','first_name','middle_name','last_name','email','salary','address','gender','job_type_id']
    
#--------EndEmp----------
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
    
    
class UsersApiView(generics.ListAPIView ):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filter.DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    filterset_fields = ['username']
    search_fields = ['username']
    ordering_fields = ['username' , 'id']
    
class UserApiView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    # def get(self , request , id):
    #     if(id):
    #         user = User.objects.all(pk=id)
    #         serializedUser = UserSerializer(user)
    #         return Response(serializedUser.data , status=status.HTTP_200_OK)
    #     else:
    #         return Response({"message" : "something went wrong"})
    
class BranchsAPIView(generics.ListAPIView , generics.ListCreateAPIView ):
    queryset= Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = [filter.DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    filterset_fields = ["id" , "number" ,"city" , "area" , "street" , "manager"]
    search_fields = ["id" , "number" , "location"  , "area" , "street" ]
    ordering_fields = ["id" , "number" ,"city" , "area" , "street" , "manager"]
    
class BranchAPIView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= Branch.objects.all()
    serializer_class = BranchSerializer
    
    
class CitiesAPIView(generics.ListAPIView , generics.ListCreateAPIView ):
    queryset= City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [filter.DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    filterset_fields = ["id" ,"city_name"]
    search_fields = ["id" , "city_name"]
    ordering_fields = ["id" ,"city_name"]
  
class CityAPIView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= City.objects.all()
    serializer_class = CitySerializer
        
    