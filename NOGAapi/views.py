from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from .serializers import UserSerializer
from django_filters import rest_framework as filter
from rest_framework import filters
from .models import *
from .serializers import *
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.views import TokenObtainPairView 
from .authentication import create_access_token , create_refresh_token
from .permissions import *
from .pagenation import Paginator
# Create your views here.


# ----------------------job type------------------------


class Job_TypesView(generics.ListAPIView,generics.ListCreateAPIView ):
    queryset=Job_Type.objects.all()
    serializer_class=Job_TypeSerializer
    permission_classes=[IsHR]
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend]
    filterset_fields=['id','job_type']
  
class Job_TypeView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= Job_Type.objects.all()
    permission_classes=[IsHR]
    serializer_class = Job_TypeSerializer
    
    def delete(self, request, pk):
        NOT_DELETABLE = ['CEO' , 'HR' , 'Manager' , 'Warehouse Administrator' , 'Sales Officer' ]
        try:
            instance = Job_Type.objects.get(pk=pk)
            if instance.job_type in NOT_DELETABLE :
                return Response({"error": "Object cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                instance.delete()
                return Response({"message": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


  
# ----------------------employee------------------------
    
class EmployeesApiView(generics.ListAPIView,generics.ListCreateAPIView):
    queryset=Employee.objects.all().select_related( 'job_type', 'branch', 'manager_of_branch', 'user', 'user_employee')
    serializer_class=EmployeeSerializer
    permission_classes=[IsHROrCEO , PermissionOnEmployees]
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['id' , 'national_number','first_name','middle_name','last_name','email','salary','address','gender','job_type' , 'branch' , 'phone']
    search_fields=['id' , 'national_number','first_name','middle_name','last_name','email','salary','address','gender' , 'phone' ]
    ordering_fields=['id' , 'national_number','first_name','middle_name','last_name','email','salary','address','gender','job_type' , 'branch' , 'phone']
    

class EmployeeApiView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset=Employee.objects.all()
    permission_classes=[IsHROrCEO , PermissionOnEmployees]
    serializer_class=EmployeeSerializer  
    
    # def put(self, request, *args, **kwargs):
    #     employee = self.get_object()
    #     data = request.data
    #     job_type = Job_Type.objects.get(id = data['job_type'])
    #     if(not request.user.is_staff):
    #         if(hasattr(request.user.employee , 'job_type')):
    #             if(request.user.employee.job_type.job_type == "HR"):
    #                 if(job_type.job_type in ["CEO" , 'Warehouse Administrator']):
    #                     return Response({
    #                         "job_type": "You do not have permission to change the job type."
    #                     }) 
                        
    #     return self.update(request, *args, **kwargs)
        # employee.national_number= data['national_number']
        # employee.first_name= data['first_name']
        # employee.middle_name= data['middle_name']
        # employee.last_name= data['last_name']
        # employee.email= data['email']
        # employee.birth_date= data['birth_date']
        # employee.gender = data['gender']
        # employee.salary= data['salary']
        # employee.address = data['address']
        # employee.branch = data['branch']
        # employee.phone = data['phone']
        
        # employee.date_of_employment= data['date_of_employment']
        # employee.job_type= Job_Type.objects.get(id=data['job_type'])  
        # employee.save()
        # serialized_data = EmployeeSerializer(employee)
        # # serialized_data.is_valid(raise_exception=True)
        # return Response(serialized_data.data)
#--------EndEmp----------

# ----------------------auth------------------------

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

# ----------------------user------------------------
    
class UsersApiView(generics.ListAPIView ):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsHROrCEO]
    pagination_class = Paginator
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
    
# ----------------------branch------------------------
    

class BranchsAPIView(generics.ListAPIView , generics.ListCreateAPIView ):
    queryset= Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes=[IsCEO]
    pagination_class = Paginator
    filter_backends = [filter.DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    filterset_fields = ["id" , "number" ,"city" , "area" , "street" , "manager"]
    search_fields = ["id" , "number" , "location"  , "area" , "street" ]
    ordering_fields = ["id" , "number" ,"city" , "area" , "street" , "manager"]
    
    
class BranchAPIView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= Branch.objects.all()
    permission_classes=[IsCEO]
    serializer_class = BranchSerializer

@api_view(['GET'])
def getAvailableManagers(request):
    employees = Employee.objects.all()
    managers = employees.filter(job_type = 4)
    serializedManagers = EmployeeSerializer(managers , many=True)
    managers = serializedManagers.data
    
    branches = Branch.objects.all()
    serializedBranches = BranchSerializer(branches , many=True)
    branches = serializedBranches.data
    
    unAvailableManagers = [branch['manager'] for branch in branches ]
    availableManagers = [manager for manager in managers if manager['id'] not in unAvailableManagers ]
    
    
    
    # managers = Employee.objects.all()
    # availableManagers = managers.filter(job_type = 4 , branch = "null")
    # availableManagers = EmployeeSerializer(availableManagers , many=True)
    # print(availableManagers.data)
    return Response({
        "results" : availableManagers
    })
    
    
# ----------------------city------------------------
    
class CitiesAPIView(generics.ListAPIView , generics.ListCreateAPIView ):
    queryset= City.objects.all()
    permission_classes=[IsCEO]
    serializer_class = CitySerializer
    filter_backends = [filter.DjangoFilterBackend , filters.SearchFilter , filters.OrderingFilter]
    pagination_class = Paginator
    filterset_fields = ["id" ,"city_name"]
    search_fields = ["id" , "city_name"]
    ordering_fields = ["id" ,"city_name"]
  
class CityAPIView( generics.RetrieveAPIView, generics.DestroyAPIView , generics.UpdateAPIView ):
    queryset= City.objects.all()
    permission_classes=[IsCEO]
    serializer_class = CitySerializer
    
# ----------------------customer------------------------
    
class CustomersApiView(generics.ListCreateAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['id' ,'national_number','first_name','middle_name','last_name']
    search_fields = ['national_number','first_name','last_name'] 
    ordering_fields = ['id' ,'national_number','first_name','last_name'] 

class CustomerApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    
    
# ----------------------products------------------------


class ProductsApiview(generics.ListCreateAPIView):
    queryset=Product.objects.all().select_related("phone" , 'accessory')
    serializer_class=ProductSerializer
    permission_classes=[IsWarehouseAdministrator]
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['product_name','wholesale_price','selling_price','quantity' , 'category_type' , 'phone__CPU_name' , 'phone__RAM' , 'phone__storage' , 'phone__battery' , 'phone__sim' , 'phone__display_size' , 'phone__sd_card' , 'phone__description' , 'phone__release_date' , 'phone__brand_id' , 'phone__CPU_id' , 'phone__color_id' , 'accessory__description' , 'accessory__accessory_category']
    search_fields = ['product_name','wholesale_price','selling_price','quantity' , 'category_type' , 'phone__CPU_name' , 'phone__RAM' , 'phone__storage' , 'phone__battery' , 'phone__sim' , 'phone__display_size' , 'phone__sd_card' , 'phone__description' , 'phone__release_date' , 'phone__brand_id' , 'phone__CPU_id' , 'phone__color_id' , 'accessory__description' , 'accessory__accessory_category'] 
    ordering_fields = ['product_name','wholesale_price','selling_price','quantity' , 'category_type' , 'phone__CPU_name' , 'phone__RAM' , 'phone__storage' , 'phone__battery' , 'phone__sim' , 'phone__display_size' , 'phone__sd_card' , 'phone__description' , 'phone__release_date' , 'phone__brand_id' , 'phone__CPU_id' , 'phone__color_id' , 'accessory__description' , 'accessory__accessory_category']
    # def get(self, request, *args, **kwargs):
    #     queryset=Product.objects.all().select_related("phone")
    #     s = ProductSerializer(queryset , many=True)
    #     print(s)
    #     return Response({"result" : s.data})
    
class ProductApiview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
# ----------------------product categories------------------------

class ProductsCategoriesApiView(generics.ListCreateAPIView):
    queryset=Products_Categories.objects.all()
    permission_classes=[IsWarehouseAdministrator]
    serializer_class=ProductCategorySerializer
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['category_name']
    search_fields = ['category_name']
    ordering_fields = ['category_name' , 'id']

class ProductCategoryApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Products_Categories.objects.all()
    serializer_class=ProductCategorySerializer
    
    
#products 

# ----------------------Phone Brands------------------------


class PhoneBrandsAPIView(generics.ListCreateAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Phone_Brand.objects.all()
    serializer_class=PhoneBrandSerializer
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['brand_name']
    search_fields = ['brand_name']
    ordering_fields = ['brand_name' , 'id']
    
class PhoneBrandAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Phone_Brand.objects.all()
    serializer_class=PhoneBrandSerializer

        
# -----------------------Colors-----------------------

class ColorsAPIView(generics.ListCreateAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Color.objects.all()
    serializer_class=ColorSerializer
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['color']
    search_fields = ['color']
    ordering_fields = ['color' , 'id']
    
class ColorAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Color.objects.all()
    serializer_class=ColorSerializer
    
# -----------------------CPU-----------------------

class CPUsAPIView(generics.ListCreateAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=CPU.objects.all()
    serializer_class=CPUSerializer
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['CPU_brand']
    search_fields = ['CPU_brand']
    ordering_fields = ['CPU_brand' , 'id']
    
class CPUAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=CPU.objects.all()
    serializer_class=CPUSerializer
    
# -----------------------Phone-----------------------




class PhonesAPIView(generics.ListCreateAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Phone.objects.all()
    serializer_class=PhoneSerializer
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['CPU_name' , 'RAM' , 'storage' , 'battery' , 'sim' , 'display_size' , 'sd_card' , 'description' , 'release_date' , 'brand_id' , 'CPU_id' , 'color_id'  ]
    search_fields = ['CPU_name' , 'RAM' , 'storage' , 'battery' , 'sim' , 'display_size' , 'sd_card' , 'description' , 'release_date' , 'brand_id' , 'CPU_id' , 'color_id' ] 
    ordering_fields = ['CPU_name' , 'RAM' , 'storage' , 'battery' , 'sim' , 'display_size' , 'sd_card' , 'description' , 'release_date' , 'brand_id' , 'CPU_id' , 'color_id' ]
    
class PhoneAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Phone.objects.all()
    serializer_class=PhoneSerializer
    
    
# -----------------------Accessory-----------------------

class AccessoriesAPIView(generics.ListCreateAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Accessory.objects.all()
    serializer_class=AccessorySerializer
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['product_id' , 'description' , 'accessory_category']
    search_fields = ['product_id' , 'description' , 'accessory_category'] 
    ordering_fields = ['product_id' , 'description' , 'accessory_category']
    
class AccessoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Accessory.objects.all()
    serializer_class=AccessorySerializer
    
    
# -----------------------Accessory category-----------------------
    
class AccessoriesCategoriesAPIView(generics.ListCreateAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Accessory_Category.objects.all()
    serializer_class=AccessoryCategorySerializer
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['category_name' ]
    search_fields =['category_name' , 'id']
    ordering_fields = ['category_name' , 'id']
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
class AccessoryCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Accessory_Category.objects.all()
    serializer_class=AccessoryCategorySerializer
    
    
# -----------------------Product------------------------------


# @api_view(['GET' , 'POST'])
# def fullProductAPIView(request):
#     data = request.data
#     product = ProductSerializer(data=data)
#     product.is_valid(raise_exception=True)
#     print(product.data['category_name'] == 'Phone')
#     if product.data['category_name'] == 'Phone':
#         phone = PhoneSerializer(data=data)
#         phone.is_valid(raise_exception=True)
#         print(phone.data)
    
#     return Response({
#         "result" : data
#     })
    
    