from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import UserSerializer
from django_filters import rest_framework as filter
from rest_framework import filters
from .models import User , Job_Type , Employee , Branch , City 
from .serializers import Job_TypeSerializer , EmployeeSerializer ,BranchSerializer , CitySerializer , MyTokenObtainPairSerializer
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.views import TokenObtainPairView 
from .authentication import create_access_token , create_refresh_token
from .permissions import IsManager , IsHR , IsSalesOfficer , IsCEO , IsSalesOfficerOrCEO , IsHROrCEO
# Create your views here.
# --------Employees---------

class Job_TypesView(generics.ListAPIView,generics.ListCreateAPIView ):
    queryset=Job_Type.objects.all()
    serializer_class=Job_TypeSerializer
    permission_classes=[IsCEO]
    filter_backends=[filter.DjangoFilterBackend]
    filterset_fields=['id','job_type']


class Job_TypeView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= Job_Type.objects.all()
    permission_classes=[IsCEO]
    serializer_class = Job_TypeSerializer
    # def destroy(self, request, *args, **kwargs):
    #     print(self)
    #     # return super().destroy(request, *args, **kwargs)
    
class EmployeesApiView(generics.ListAPIView,generics.ListCreateAPIView):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    permission_classes=[IsHROrCEO]
    filter_backends=[filter.DjangoFilterBackend]
    filterset_fields=['id' , 'national_number','first_name','middle_name','last_name','email','salary','address','gender','job_type']

class EmployeeApiView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset=Employee.objects.all()
    permission_classes=[IsHROrCEO]
    serializer_class=EmployeeSerializer    
#--------EndEmp----------

#-------Auth-------------
class RrgisterAPIView(APIView):
    permission_classes=[IsHROrCEO]
    def post(self , requset):
        data = requset.data
        # employee = data["employee"]
        
        if(data["password"] != data["confirm_password"]):
            return Response({
                "validationError" : "password and confirm_password don't macth",
            })
        serializedData = UserSerializer(data=requset.data)
        serializedData.is_valid(raise_exception=True)
        serializedData.save()
        
        return Response(serializedData.data , status=status.HTTP_200_OK)
    
    
class LoginAPIView(APIView):
    def post(self , request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed("invalid inputs")
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong inputs")
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return Response({
            "access_token": access_token,
            "refresh_token" : refresh_token
            })
#-------EndAuth-------------
    
class UsersApiView(generics.ListAPIView ):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsCEO]
    filter_backends = [filter.DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    filterset_fields = ['username']
    search_fields = ['username']
    ordering_fields = ['username' , 'id']
    
class UserApiView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= User.objects.all()
    permission_classes=[IsCEO]
    serializer_class = UserSerializer
    # def get(self , request , id):
    #     if(id):
    #         user = User.objects.all(pk=id)
    #         serializedUser = UserSerializer(user)
    #         return Response(serializedUser.data , status=status.HTTP_200_OK)
    #     else:
    #         return Response({"message" : "something went wrong"})
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
    
    

class BranchsAPIView(generics.ListAPIView , generics.ListCreateAPIView ):
    queryset= Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes=[IsCEO]
    filter_backends = [filter.DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    filterset_fields = ["id" , "number" ,"city" , "area" , "street" , "manager"]
    search_fields = ["id" , "number" , "location"  , "area" , "street" ]
    ordering_fields = ["id" , "number" ,"city" , "area" , "street" , "manager"]
    
class BranchAPIView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= Branch.objects.all()
    permission_classes=[IsCEO]
    serializer_class = BranchSerializer
    
    
class CitiesAPIView(generics.ListAPIView , generics.ListCreateAPIView ):
    queryset= City.objects.all()
    permission_classes=[IsCEO]
    serializer_class = CitySerializer
    filter_backends = [filter.DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    filterset_fields = ["id" ,"city_name"]
    search_fields = ["id" , "city_name"]
    ordering_fields = ["id" ,"city_name"]
  
class CityAPIView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= City.objects.all()
    permission_classes=[IsCEO]
    serializer_class = CitySerializer
        
    