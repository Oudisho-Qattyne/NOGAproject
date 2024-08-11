from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
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
from django.db.models.functions import TruncMonth
from django.db.models import Count , Sum , ExpressionWrapper , F
from django.db.models.functions import Concat
# from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

def validate_date_format(date_str):
    try:
        # Validate the date format as "yyyy-mm-dd"
        datetime.strptime(date_str, '%Y-%m-%d')
        return True  # Return True if the format is correct
    except ValueError:
        return False  # Return False if the format is incorrect

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
    # parser_classes = (MultiPartParser, FormParser)
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
    filterset_fields=['id' ,'national_number','first_name','middle_name','last_name' , 'phone' , 'gender']
    search_fields = ['national_number','first_name','middle_name','last_name' , 'phone'] 
    ordering_fields = ['id' ,'national_number','first_name','middle_name','last_name' , 'phone' , 'gender'] 

class CustomerApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    
    
# ----------------------products------------------------


class ProductsApiview(generics.ListCreateAPIView):
    queryset=Product.objects.all().select_related("phone" , 'accessory')
    serializer_class=ProductSerializer
    permission_classes=[IsWarehouseAdministrator]
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter ]
    search_fields = ['product_name','wholesale_price','selling_price','quantity'  , 'category_type__category_name', 'phone__CPU_name' , 'phone__RAM' , 'phone__storage' , 'phone__battery' , 'phone__sim' , 'phone__display_size' , 'phone__sd_card' , 'phone__description' , 'phone__release_date' , 'phone__brand_id__brand_name' , 'phone__CPU_id__CPU_brand' , 'phone__color_id__color' , 'accessory__description' , 'accessory__accessory_category__category_name'] 
    filterset_fields = ['id','product_name','wholesale_price','selling_price','quantity'  , 'category_type' , 'phone__CPU_name' , 'phone__RAM' , 'phone__storage' , 'phone__battery' , 'phone__sim' , 'phone__display_size' , 'phone__sd_card' , 'phone__description' , 'phone__release_date' , 'phone__brand_id' , 'phone__CPU_id' , 'phone__color_id' , 'accessory__description' , 'accessory__accessory_category']
    ordering_fields = ['product_name','wholesale_price','selling_price','quantity'  , 'category_type' , 'phone__CPU_name' , 'phone__RAM' , 'phone__storage' , 'phone__battery' , 'phone__sim' , 'phone__display_size' , 'phone__sd_card' , 'phone__description' , 'phone__release_date' , 'phone__brand_id' , 'phone__CPU_id' , 'phone__color_id' , 'accessory__description' , 'accessory__accessory_category']
    # def get(self, request, *args, **kwargs):
    #     queryset=Product.objects.all().select_related("phone")
    #     s = ProductSerializer(queryset , many=True)
    #     print(s)
    #     return Response({"result" : s.data})
    def get_queryset(self):
        queryset = Product.objects.all()
        min_value = self.request.query_params.get('min_price')
        max_value = self.request.query_params.get('max_price')
        
        if min_value is not None:
            queryset = queryset.filter(wholesale_price__gte=min_value)
        if max_value is not None:
            queryset = queryset.filter(wholesale_price__lte=max_value)
       
            
        return queryset
class ProductApiview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsWarehouseAdministrator]
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
# ----------------------product entry to the main storage------------------------

class EntryProcessApiView(generics.ListCreateAPIView):
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['id' , 'date_of_process']
    search_fields = ['id' , 'date_of_process'] 
    ordering_fields = ['id' , 'date_of_process']
    permission_classes=[IsAuthenticated]
    queryset=Entry_process.objects.all()
    serializer_class=EntryProcessSerializer
    

# ----------------------product movment to the branches's storage------------------------


class ProductsMovmentApiView(generics.ListCreateAPIView):
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['branch__id' , 'movement_type' , 'date_of_process']
    search_fields = ['branch__id' ,'movement_type' , 'date_of_process'] 
    ordering_fields = ['branch__id' , 'movement_type' , 'date_of_process']
    queryset=Products_Movment.objects.all().order_by('-date_of_process')
    serializer_class=ProductsMovmentSerializer
    permission_classes=[IsAuthenticated]
# ----------------------product movment to the branches's storage------------------------
class BranchesProductsApiView(generics.ListAPIView):
    pagination_class = Paginator
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter ]

    search_fields = [ 'branch__id' , 'quantity' , 'product__category_type__category_name', 'product__product_name' , 'product__wholesale_price','product__selling_price'  , 'product__phone__RAM' , 'product__phone__storage' , 'product__phone__battery' , 'product__phone__sim' , 'product__phone__display_size' , 'product__phone__sd_card' , 'product__phone__description' , 'product__phone__release_date' , 'product__phone__brand_id__brand_name' , 'product__phone__CPU_id__CPU_brand' , 'product__phone__color_id__color' , 'product__accessory__description' , 'product__accessory__accessory_category__category_name'] 
    filterset_fields = ['product__id', 'branch__id' , 'quantity' , 'product__category_type', 'product__product_name' , 'product__wholesale_price','product__selling_price'  , 'product__phone__RAM' , 'product__phone__storage' , 'product__phone__battery' , 'product__phone__sim' , 'product__phone__display_size' , 'product__phone__sd_card' , 'product__phone__description' , 'product__phone__release_date' , 'product__phone__brand_id' , 'product__phone__CPU_id' , 'product__phone__color_id' , 'product__accessory__description' , 'product__accessory__accessory_category'] 
    ordering_fields = [ 'branch__id' , 'quantity' , 'product__category_type', 'product__product_name' , 'product__wholesale_price','product__selling_price'  , 'product__phone__RAM' , 'product__phone__storage' , 'product__phone__battery' , 'product__phone__sim' , 'product__phone__display_size' , 'product__phone__sd_card' , 'product__phone__description' , 'product__phone__release_date' , 'product__phone__brand_id' , 'product__phone__CPU_id' , 'product__phone__color_id' , 'product__accessory__description' , 'product__accessory__accessory_category'] 

    queryset=Branch_Products.objects.all()
    serializer_class=BranchProductsSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        queryset = Branch_Products.objects.all()
        min_value = self.request.query_params.get('min_price')
        max_value = self.request.query_params.get('max_price')
        
        if min_value is not None:
            queryset = queryset.filter(product__selling_price__gte=min_value)
        if max_value is not None:
            queryset = queryset.filter(product__selling_price__lte=max_value)
       
            
        return queryset
    
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
    filterset_fields=['product' , 'description' , 'accessory_category']
    search_fields = ['product' , 'description' , 'accessory_category'] 
    ordering_fields = ['product' , 'description' , 'accessory_category']
    
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
    
class BranchesRequestsAPIView(generics.ListCreateAPIView):
    pagination_class = Paginator
    queryset=Branches_Requests.objects.all().order_by('-date_of_request')
    serializer_class=BranchesRequestsSerializer
    filter_backends=[filter.DjangoFilterBackend, filters.SearchFilter , filters.OrderingFilter]
    filterset_fields=['branch_id' , 'date_of_request' , 'processed']
    search_fields = ['branch_id' , 'date_of_request' , 'note'] 
    ordering_fields = ['branch_id' , 'date_of_request' , 'processed']
    
class BrancheRequestAPIView(generics.RetrieveAPIView):
    queryset=Branches_Requests.objects.all()
    serializer_class=BranchesRequestsSerializer

class RequestStatusAPIView(generics.ListCreateAPIView):
    queryset=Request_Status.objects.all()
    serializer_class=RequestStatusSerializer

@api_view(['POST'])
def RejectAllRequistedProducts(request):
    if 'request_id' not in request.data:
        return Response({"request_id" : "required"} , status=status.HTTP_400_BAD_REQUEST)
        
    request_id = request.data['request_id']
    requested_products_instances = Requested_Products.objects.filter(request_id=request_id)
    if len(requested_products_instances) == 0:
        return Response({'error': 'this request has no products requests '}, status=status.HTTP_404_NOT_FOUND)
    request_status_pending = Request_Status.objects.get(id=1) 
    request_status_fully_accept = Request_Status.objects.get(id=2) 
    request_status_partly_accept = Request_Status.objects.get(id=3) 
    request_status_reject = Request_Status.objects.get(id=4) 
    error = {
        "products_requests" : []
    }
    
    for index , requested_products_instance in enumerate(requested_products_instances):
        if  requested_products_instance.status in [request_status_partly_accept, request_status_fully_accept]:
            error['products_requests'].append({index+1 : "product request already processed"})
            
    if len(error['products_requests']) > 0:
        return Response(error , status=status.HTTP_400_BAD_REQUEST)
    
    for requested_products_instance in requested_products_instances:
        requested_products_instance.status = request_status_reject
        requested_products_instance.save()
    branches_requests_instance = Branches_Requests.objects.get(id=request_id)
    branches_requests_instance.processed = True
    branches_requests_instance.save()
    
    return Response({"message" : "all requests are rejected" }, status=status.HTTP_200_OK )

@api_view(['POST'])
@permission_classes([IsWarehouseAdministrator])
def RejectRequistedProduct(request):
    if 'product_request_id' not in request.data:
        return Response({"product_request_id" : "required"} , status=status.HTTP_400_BAD_REQUEST)
        
    
    product_request_id = request.data['product_request_id']
    request_status_pending = Request_Status.objects.get(id=1) 
    request_status_fully_accept = Request_Status.objects.get(id=2) 
    request_status_partly_accept = Request_Status.objects.get(id=3) 
    request_status_reject = Request_Status.objects.get(id=4) 
    try:
        products_request_instance = Requested_Products.objects.get(id=product_request_id)
        if products_request_instance.status in [request_status_fully_accept , request_status_partly_accept , request_status_reject] :
            return Response({"message" : "product request already processed"} , status=status.HTTP_400_BAD_REQUEST)
        products_request_instance.status = request_status_reject
        products_request_instance.save()
        
        requested_products_instances = Requested_Products.objects.filter(request_id=products_request_instance.request_id.id)
        branch_request = Branches_Requests.objects.get(id=products_request_instance.request_id.id)
        
        pending_requests = False
        for requested_products_instance in requested_products_instances:
            if requested_products_instance.status == request_status_pending:
                pending_requests = True
                break
        
        if pending_requests:
            branch_request.processed = False
        else :
            branch_request.processed = True
            
        branch_request.save()
        
        return Response({"message" : "rejected" }, status=status.HTTP_200_OK )

    except Requested_Products.DoesNotExist:
        return Response({'error': 'product request not found'}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])
@permission_classes([IsWarehouseAdministrator])
def ProcessRequestedProduct(request):
    if 'product_request_id' not in request.data:
        return Response({"product_request_id" : "required"} , status=status.HTTP_400_BAD_REQUEST)

    if 'quantity' not in request.data:
        return Response({"quantity" : "required"} , status=status.HTTP_400_BAD_REQUEST)
    
    product_request_id = request.data['product_request_id']
    quantity = request.data['quantity']
    if quantity <= 0:
        return Response({"quantity" : "invalid quantity"} , status=status.HTTP_400_BAD_REQUEST)
        
    request_status_pending = Request_Status.objects.get(id=1) 
    request_status_fully_accept = Request_Status.objects.get(id=2) 
    request_status_partly_accept = Request_Status.objects.get(id=3) 
    request_status_reject = Request_Status.objects.get(id=4) 
    try:
        products_request_instance = Requested_Products.objects.get(id=product_request_id)
        try:
            product_instance = Product.objects.get(id=products_request_instance.product_id.id)
        except Product.DoesNotExist:
            return Response({'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            branch_request = Branches_Requests.objects.get(id=products_request_instance.request_id.id)
        except Branches_Requests.DoesNotExist:
            return Response({'error': 'request not found'}, status=status.HTTP_404_NOT_FOUND)
            
        if products_request_instance.status in [request_status_fully_accept , request_status_partly_accept , request_status_reject] :
            return Response({"message" : "product request already processed"} , status=status.HTTP_400_BAD_REQUEST)
        if quantity > product_instance.quantity:
            return Response({"message" : f"we don't have this quantity in the main warehouse, we have only {product_instance.quantity}"} , status=status.HTTP_400_BAD_REQUEST)
        
        products_movment_instance = Products_Movment.objects.create(branch=branch_request.branch_id , movement_type=True)    
        transported_product_instance = Transported_Product.objects.create(process = products_movment_instance , product=product_instance , wholesale_price=product_instance.wholesale_price , selling_price=product_instance.selling_price , quantity=products_request_instance.quantity)
        try:
            branch_product_instance = Branch_Products.objects.get(branch=products_movment_instance.branch , product=transported_product_instance.product)
            branch_product_instance.quantity += quantity
            product_instance.quantity -= quantity
        except Branch_Products.DoesNotExist:
            branch_product_instance = Branch_Products.objects.create(product=transported_product_instance.product , branch = products_movment_instance.branch , quantity = transported_product_instance.quantity)
            product_instance.quantity -= quantity
            
        requested_products_instances = Requested_Products.objects.filter(request_id=branch_request.id)
        pending_requests = False
        for requested_products_instance in requested_products_instances:
            if requested_products_instance.status == request_status_pending:
                pending_requests = True
                break
        
        if pending_requests:
            branch_request.processed = False
        else :
            branch_request.processed = True
            
        branch_request.save()
        
        transported_product_instance.save()
        branch_product_instance.save()
        product_instance.save()
        message = {"message" : "accepted" }
        if products_request_instance.quantity > quantity:
            products_request_instance.status = request_status_partly_accept
            message['message'] = 'partly_accepted'
        elif products_request_instance.quantity <= quantity:
            products_request_instance.status = request_status_fully_accept
            message['message'] = 'fully_accepted'
        
        products_request_instance.save()
            
        return Response(message, status=status.HTTP_200_OK )

    except Requested_Products.DoesNotExist:
        return Response({'error': 'product request not found'}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])
@permission_classes([IsWarehouseAdministrator])
def ProcessAllRequestedProducts(request):
    if 'request_id' not in request.data:
        return Response({"request_id" : "required"} , status=status.HTTP_400_BAD_REQUEST)
    request_id = request.data['request_id']
    
    request_status_pending = Request_Status.objects.get(id=1) 
    request_status_fully_accept = Request_Status.objects.get(id=2) 
    request_status_partly_accept = Request_Status.objects.get(id=3) 
    request_status_reject = Request_Status.objects.get(id=4) 
    error = {
        "products_requests" : []
    }
    try:
        branch_request = Branches_Requests.objects.get(id=request_id)
    except Branches_Requests.DoesNotExist:
        return Response({'error': 'request not found'}, status=status.HTTP_404_NOT_FOUND)
    requested_products_instances = Requested_Products.objects.filter(request_id=request_id)
    
    if len(requested_products_instances) == 0:
        return Response({'error': 'this request has no products requests '}, status=status.HTTP_404_NOT_FOUND)
    
    for index , requested_products_instance in enumerate(requested_products_instances):
        try:
            product_instance = Product.objects.get(id=requested_products_instance.product_id.id)
            if  requested_products_instance.status in [request_status_partly_accept, request_status_fully_accept]:
                error['products_requests'].append({index+1 : "product request already processed"})
            if product_instance.quantity < requested_products_instance.quantity:
                error['products_requests'].append({index+1 : f"we don't have this quantity in the main warehouse, we have only {product_instance.quantity}"})    
        except Product.DoesNotExist:
            error['products_requests'].append({index: 'product not found'})
       
    if len(error['products_requests']) > 0:
        return Response(error , status=status.HTTP_400_BAD_REQUEST)
    
    for requested_products_instance in requested_products_instances:
        product_instance = Product.objects.get(id=requested_products_instance.product_id.id)
        products_movment_instance = Products_Movment.objects.create(branch=branch_request.branch_id , movement_type=True)    
        transported_product_instance = Transported_Product.objects.create(process = products_movment_instance , product=product_instance , wholesale_price=product_instance.wholesale_price , selling_price=product_instance.selling_price , quantity=requested_products_instance.quantity)
        try:
            branch_product_instance = Branch_Products.objects.get(branch=products_movment_instance.branch , product=transported_product_instance.product)
            branch_product_instance.quantity += requested_products_instance.quantity
            product_instance.quantity -= requested_products_instance.quantity
        except Branch_Products.DoesNotExist:
            branch_product_instance = Branch_Products.objects.create(product=transported_product_instance.product , branch = products_movment_instance.branch , quantity = transported_product_instance.quantity)
            product_instance.quantity -= requested_products_instance.quantity
        products_movment_instance.save()
        transported_product_instance.save()
        branch_product_instance.save()
        product_instance.save()
        branches_requests_instance = Branches_Requests.objects.get(id=request_id)
        branches_requests_instance.processed = True
        branches_requests_instance.save()
        requested_products_instance.status = request_status_fully_accept
        requested_products_instance.save()
    return Response({"message" : "all requests are fully accepted" }, status=status.HTTP_200_OK )
        

#-------------------
#------------purchase----------
class PurchaseAPIView(generics.ListCreateAPIView):
    queryset=Purchase.objects.all()
    pagination_class = Paginator
    serializer_class=PurchaseSerializer
    
    
#---------ststistics--------
@api_view(["GET"])
def TotalIncome(request):
    # branch_id = request.query_params.get('branch_id', None)
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    day = request.query_params.get('day', None)
    statistics=Purchased_Products.objects.all()
    if month:
        if validate_date_format(month):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = month.split('-')[0] , purchase_id__date_of_purchase__month = month.split('-')[1])
            statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
            if(statistics['total_income']):
                return(Response(statistics))
            else:
                return(Response({'total_income':0.0}))
        else: 
            return Response({"month" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif year:
        if validate_date_format(year):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = year.split('-')[0])
            
            statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
            if(statistics['total_income']):
                return(Response(statistics))
            else:
                return(Response({'total_income':0.0}))
        else: 
            return Response({"year" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif day:
        if validate_date_format(day):
            statistics = statistics.filter( purchase_id__date_of_purchase__year = day.split('-')[0] , purchase_id__date_of_purchase__day = day.split('-')[2] ,  purchase_id__date_of_purchase__month = day.split('-')[1])
            
            statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
            if(statistics['total_income']):
                return(Response(statistics))
            else:
                return(Response({'total_income':0.0}))
        else: 
            return Response({"day" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
        if(statistics['total_income']):
            return(Response(statistics))
        else:
            return(Response({'total_income':0.0}))
        
        
@api_view(["GET"])
def TotalIncomePerBranch(request , branch_id):
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    day = request.query_params.get('day', None)
    
    statistics=Purchased_Products.objects.filter(purchase_id__branch_id=branch_id)
    if month:
        if validate_date_format(month):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = month.split('-')[0] ,purchase_id__date_of_purchase__month = month.split('-')[1])
            statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
            if(statistics['total_income']):
                return(Response(statistics))
            else:
                return(Response({'total_income':0.0}))
        else: 
            return Response({"month" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif year:
        if validate_date_format(year):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = year.split('-')[0])
            statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
            if(statistics['total_income']):
                return(Response(statistics))
            else:
                return(Response({'total_income':0.0}))
        else: 
            return Response({"year" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif day:
        if validate_date_format(day):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = day.split('-')[0] ,purchase_id__date_of_purchase__day = day.split('-')[2] , purchase_id__date_of_purchase__month = day.split('-')[1])
            
            statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
            if(statistics['total_income']):
                return(Response(statistics))
            else:
                return(Response({'total_income':0.0}))
        else: 
            return Response({"day" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
        if(statistics['total_income']):
            return(Response(statistics))
        else:
            return(Response({'total_income':0.0}))
        

@api_view(["GET"])
def TotalIncomeAllBranch(request):
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    day = request.query_params.get('day', None)
    
    statistics=Purchased_Products.objects.all()
    if month:
        if validate_date_format(month):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = month.split('-')[0] ,purchase_id__date_of_purchase__month = month.split('-')[1])
            # statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
            statistics=statistics.values("purchase_id__branch_id"  ).annotate(branch_id = ExpressionWrapper(F("purchase_id__branch_id") , output_field=models.CharField(max_length=10)) ).values('branch_id').annotate(total=Sum(ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField())) ).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100)))
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response({'total_income':0.0}))
        else: 
            return Response({"month" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif year:
        if validate_date_format(year):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = year.split('-')[0])
            statistics=statistics.values("purchase_id__branch_id"  ).annotate(branch_id = ExpressionWrapper(F("purchase_id__branch_id") , output_field=models.CharField(max_length=10)) ).values('branch_id').annotate(total=Sum(ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField())) ).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100)))
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response({'total_income':0.0}))
        else: 
            return Response({"year" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif day:
        if validate_date_format(day):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = day.split('-')[0] ,purchase_id__date_of_purchase__day = day.split('-')[2] , purchase_id__date_of_purchase__month = day.split('-')[1])
            
            statistics=statistics.values("purchase_id__branch_id"  ).annotate(branch_id = ExpressionWrapper(F("purchase_id__branch_id") , output_field=models.CharField(max_length=10)) ).values('branch_id').annotate(total=Sum(ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField())) ).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100)))
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response({'total_income':0.0}))
        else: 
            return Response({"day" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        statistics=statistics.values("purchase_id__branch_id"  ).annotate(branch_id = ExpressionWrapper(F("purchase_id__branch_id") , output_field=models.CharField(max_length=10)) ).values('branch_id').annotate(total=Sum(ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField())) ).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100)))
        
        if(statistics):
            return(Response(statistics))
        else:
            return(Response({'total_income':0.0}))
 
@api_view(["GET"])
def TotaEarnings(request):
    # branch_id = request.query_params.get('branch_id', None)
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    day = request.query_params.get('day', None)
        

    statistics=Purchased_Products.objects.all()
    if month:
        if validate_date_format(month):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = month.split('-')[0] , purchase_id__date_of_purchase__month = month.split('-')[1])
            statistics = statistics.annotate(total=ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_earning = Sum('total'))
            if(statistics['total_earning']):
                return(Response(statistics))
            else:
                return(Response({'total_earning':0.0}))
        else: 
            return Response({"month" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif year:
        if validate_date_format(year):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = year.split('-')[0])
            
            statistics = statistics.annotate(total=ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_earning = Sum('total'))
            if(statistics['total_earning']):
                return(Response(statistics))
            else:
                return(Response({'total_earning':0.0}))
        else: 
            return Response({"year" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif day:
        if validate_date_format(day):
            statistics = statistics.filter( purchase_id__date_of_purchase__year = day.split('-')[0] , purchase_id__date_of_purchase__day = day.split('-')[2] ,  purchase_id__date_of_purchase__month = day.split('-')[1])
            
            statistics = statistics.annotate(total=ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_earning = Sum('total'))
            if(statistics['total_earning']):
                return(Response(statistics))
            else:
                return(Response({'total_earning':0.0}))
        else: 
            return Response({"day" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        statistics = statistics.annotate(total=ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_earning = Sum('total'))
        if(statistics['total_earning']):
            return(Response(statistics))
        else:
            return(Response({'total_earning':0.0}))
   
  
@api_view(["GET"])
def TotalEarningPerBranch(request , branch_id):
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    day = request.query_params.get('day', None)
    
    statistics=Purchased_Products.objects.filter(purchase_id__branch_id=branch_id)
    if month:
        if validate_date_format(month):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = month.split('-')[0] ,purchase_id__date_of_purchase__month = month.split('-')[1])
            statistics = statistics.annotate(total=ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField())).aggregate(total_earning = Sum('total'))
            if(statistics['total_earning']):
                return(Response(statistics))
            else:
                return(Response({'total_earning':0.0}))
        else: 
            return Response({"month" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif year:
        if validate_date_format(year):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = year.split('-')[0])
            statistics = statistics.annotate(total=ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_earning = Sum('total'))
            if(statistics['total_earning']):
                return(Response(statistics))
            else:
                return(Response({'total_earning':0.0}))
        else: 
            return Response({"year" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif day:
        if validate_date_format(day):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = day.split('-')[0] ,purchase_id__date_of_purchase__day = day.split('-')[2] , purchase_id__date_of_purchase__month = day.split('-')[1])
            
            statistics = statistics.annotate(total=ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_earning = Sum('total'))
            if(statistics['total_earning']):
                return(Response(statistics))
            else:
                return(Response({'total_earning':0.0}))
        else: 
            return Response({"day" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        statistics = statistics.annotate(total=ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_earning = Sum('total'))
        if(statistics['total_earning']):
            return(Response(statistics))
        else:
            return(Response({'total_earning':0.0}))
        
        
@api_view(["GET"])
def TotalEarningAllBranch(request):
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    day = request.query_params.get('day', None)
    
    statistics=Purchased_Products.objects.all()
    if month:
        if validate_date_format(month):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = month.split('-')[0] ,purchase_id__date_of_purchase__month = month.split('-')[1])
            # statistics = statistics.annotate(total=ExpressionWrapper(F('selling_price') * F('purchased_quantity'), output_field=models.DecimalField()) ).aggregate(total_income = Sum('total'))
            statistics=statistics.values("purchase_id__branch_id"  ).annotate(branch_id = ExpressionWrapper(F("purchase_id__branch_id") , output_field=models.CharField(max_length=10)) ).values('branch_id').annotate(total_earning=Sum(ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ) ).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100)))
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response([]))
        else: 
            return Response({"month" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif year:
        if validate_date_format(year):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = year.split('-')[0])
            statistics=statistics.values("purchase_id__branch_id"  ).annotate(branch_id = ExpressionWrapper(F("purchase_id__branch_id") , output_field=models.CharField(max_length=10)) ).values('branch_id').annotate(total_earning=Sum(ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ) ).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100)))
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response([]))
        else: 
            return Response({"year" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif day:
        if validate_date_format(day):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = day.split('-')[0] ,purchase_id__date_of_purchase__day = day.split('-')[2] , purchase_id__date_of_purchase__month = day.split('-')[1])
            
            statistics=statistics.values("purchase_id__branch_id"  ).annotate(branch_id = ExpressionWrapper(F("purchase_id__branch_id") , output_field=models.CharField(max_length=10)) ).values('branch_id').annotate(total_earning=Sum(ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ) ).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100)))
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response([]))
        else: 
            return Response({"day" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        statistics=statistics.values("purchase_id__branch_id"  ).annotate(branch_id = ExpressionWrapper(F("purchase_id__branch_id") , output_field=models.CharField(max_length=10)) ).values('branch_id').annotate(total_earning=Sum(ExpressionWrapper((F('selling_price') - F('wholesale_price')) * F('purchased_quantity'), output_field=models.DecimalField()) ) ).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100)))
            
        if(statistics):
            return(Response(statistics))
        else:
            return(Response([]))
 
@api_view(["GET"])
def TotalProducts(request):
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    day = request.query_params.get('day', None)
    
    statistics=Purchased_Products.objects.all()
    if month:
        if validate_date_format(month):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = month.split('-')[0] ,purchase_id__date_of_purchase__month = month.split('-')[1])
            statistics=statistics.values("product_id").annotate(total=Sum('purchased_quantity')).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response([]))
        else: 
            return Response({"month" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif year:
        if validate_date_format(year):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = year.split('-')[0])
            statistics=statistics.values("product_id").annotate(total=Sum('purchased_quantity')).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response([]))
        else: 
            return Response({"year" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif day:
        if validate_date_format(day):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = day.split('-')[0] ,purchase_id__date_of_purchase__day = day.split('-')[2] , purchase_id__date_of_purchase__month = day.split('-')[1])
            statistics=statistics.values("product_id").annotate(total=Sum('purchased_quantity')).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            if(statistics):
                return(Response(statistics))
            else:
                return(Response([]))
        else: 
            return Response({"day" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        statistics=statistics.values("product_id").annotate(total=Sum('purchased_quantity')).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            
        if(statistics):
            return(Response(statistics))
        else:
            return(Response([]))
 
@api_view(["GET"])
def TotalProductsPerBranch(request , branch_id):
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    day = request.query_params.get('day', None)
    
    statistics=Purchased_Products.objects.filter(purchase_id__branch_id=branch_id)

    if month:
        if validate_date_format(month):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = month.split('-')[0] ,purchase_id__date_of_purchase__month = month.split('-')[1])
            statistics=statistics.values("product_id").annotate(total=Sum('purchased_quantity')).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response([]))
        else: 
            return Response({"month" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif year:
        if validate_date_format(year):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = year.split('-')[0])
            statistics=statistics.values("product_id").annotate(total=Sum('purchased_quantity')).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            
            if(statistics):
                return(Response(statistics))
            else:
                return(Response([]))
        else: 
            return Response({"year" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif day:
        if validate_date_format(day):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = day.split('-')[0] ,purchase_id__date_of_purchase__day = day.split('-')[2] , purchase_id__date_of_purchase__month = day.split('-')[1])
            statistics=statistics.values("product_id").annotate(total=Sum('purchased_quantity')).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            if(statistics):
                return(Response(statistics))
            else:
                return(Response([]))
        else: 
            return Response({"day" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        statistics=statistics.values("product_id").annotate(total=Sum('purchased_quantity')).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            
        if(statistics):
            return(Response(statistics))
        else:
            return(Response([]))

def calcBranchesProductsQuantities(statistics):
    res = []
    branches = {}
    for branch in statistics:
        if branch['purchase_id__branch_id'] in branches.keys():
            res[branches[branch['purchase_id__branch_id']]]['products'].append(
                {
                    "product_id":branch['product_id'],
                    "product_name":branch['product_name'],
                    "total":branch['total']
                }
            )
        else:
            branches[branch['purchase_id__branch_id']] = len(res)
            res.append({
                "branch_id":branch['purchase_id__branch_id'],
                "branch_name":branch['branch_name'],
                "products":[
                    {
                        "product_id":branch['product_id'],
                        "product_name":branch['product_name'],
                        "total":branch['total']
                    }
                ]
            })
    return res

@api_view(["GET"])
def TotalProductsAllBranch(request):
    month = request.query_params.get('month', None)
    year = request.query_params.get('year', None)
    day = request.query_params.get('day', None)
    
    statistics=Purchased_Products.objects.all()

    if month:
        if validate_date_format(month):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = month.split('-')[0] ,purchase_id__date_of_purchase__month = month.split('-')[1])
            statistics=statistics.values('purchase_id__branch_id' , "product_id").annotate(total=Sum('purchased_quantity')).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100))).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            res = calcBranchesProductsQuantities(statistics)
            if(statistics):
                return(Response(res))
            else:
                return(Response([]))
        else: 
            return Response({"month" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif year:
        if validate_date_format(year):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = year.split('-')[0])
            statistics=statistics.values('purchase_id__branch_id' , "product_id").annotate(total=Sum('purchased_quantity')).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100))).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            res = calcBranchesProductsQuantities(statistics)
            if(statistics):
                return(Response(res))
            else:
                return(Response([]))
        else: 
            return Response({"year" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    elif day:
        if validate_date_format(day):
            statistics = statistics.filter(purchase_id__date_of_purchase__year = day.split('-')[0] ,purchase_id__date_of_purchase__day = day.split('-')[2] , purchase_id__date_of_purchase__month = day.split('-')[1])
            statistics=statistics.values('purchase_id__branch_id' , "product_id").annotate(total=Sum('purchased_quantity')).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100))).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
            res = calcBranchesProductsQuantities(statistics)
            if(statistics):
                return(Response(res))
            else:
                return(Response([]))
        else: 
            return Response({"day" : "invalid date" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        statistics=statistics.values('purchase_id__branch_id' , "product_id").annotate(total=Sum('purchased_quantity')).annotate(branch_name = ExpressionWrapper(Concat(F("purchase_id__branch_id__city__city_name") , F('purchase_id__branch_id__number')) , output_field=models.CharField(max_length=100))).annotate(product_name = ExpressionWrapper(F("product_id__product_name") , output_field=models.CharField(max_length=100))).order_by("-total")
        res = calcBranchesProductsQuantities(statistics)
        if(statistics):
            return(Response(res))
        else:
            return(Response([]))
 

@api_view(['GET'])
def getCustomersNumber(request):
    customers = Customer.objects.all().count()
    
    return(Response({"customers_number" : customers}))