from django.urls import path , include , re_path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [
    path('register' , RrgisterAPIView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
    # path('token' , obtain_auth_token),
    # path('login' , LoginAPIView.as_view()),
    
    
    path('users' , UsersApiView.as_view() ),
    path('users/<int:pk>' , UserApiView.as_view() ),
    
    path('employees',EmployeesApiView.as_view()),
    path('employees/<int:pk>' , EmployeeApiView.as_view() ),
    
    path('available_managers' , getAvailableManagers),
    
    
    path('job-types',Job_TypesView.as_view()),
    path('job-types/<int:pk>' , Job_TypeView.as_view() ),
    
    path('branches',BranchsAPIView.as_view()),
    path('branches/<int:pk>' , BranchAPIView.as_view() ),
    
    path('cities',CitiesAPIView.as_view()),
    path('cities/<int:pk>' , CityAPIView.as_view() ),
    
    path('customers',CustomersApiView.as_view()),
    path('customers/<int:pk>',CustomerApiView.as_view()),
    
    path('products/',ProductsApiview.as_view()),
    path('products/<int:pk>',ProductApiview.as_view()),
    
    path('products_categories/',ProductsCategoriesApiView.as_view()),
    path('products_categories/<int:pk>',ProductCategoryApiView.as_view()),
    
    path('login', MyTokenObtainPairView.as_view() , name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    #products 

# ----------------------Phone Brands------------------------

    path('phone_brands' , PhoneBrandsAPIView.as_view()),
    path('phone_brands/<int:pk>' , PhoneBrandAPIView.as_view()),
    
# -----------------------Colors-----------------------
    
    path('colors' , ColorsAPIView.as_view()),
    path('colors/<int:pk>' , ColorAPIView.as_view()),
    
# -----------------------CPU-----------------------
    
    path('cpus' , CPUsAPIView.as_view()),
    path('cpus/<int:pk>' , CPUAPIView.as_view()),
    
# -----------------------Phone-----------------------
    
    path('phones' , PhonesAPIView.as_view()),
    path('phones/<int:pk>' , PhoneAPIView.as_view()),
    
# -----------------------Accessory-----------------------

    path('accessories' , AccessoriesAPIView.as_view()),
    path('accessories/<int:pk>' , AccessoryAPIView.as_view()),
    
# -----------------------Accessory category-----------------------

    path('accessories_categories' , AccessoriesCategoriesAPIView.as_view()),
    path('accessories_categories/<int:pk>' , AccessoryCategoryAPIView.as_view()),
    
    
# -----------------------Products-----------------------
    
    path('products' , ProductsApiview.as_view()),
    # path('products/<int:pk>' , fullProductAPIView),
]