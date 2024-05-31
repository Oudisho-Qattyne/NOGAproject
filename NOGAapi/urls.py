from django.urls import path , include , re_path
from .views import RrgisterAPIView , LoginAPIView , UsersApiView , UserApiView , EmployeesApiView , EmployeeApiView , Job_TypesView , Job_TypeView , BranchsAPIView , BranchAPIView , CitiesAPIView , CityAPIView
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
    path('job-types',Job_TypesView.as_view()),
    path('job-types/<int:pk>' , Job_TypeView.as_view() ),
    path('branchs',BranchsAPIView.as_view()),
    path('branchs/<int:pk>' , BranchAPIView.as_view() ),
    path('cities',CitiesAPIView.as_view()),
    path('cities/<int:pk>' , CityAPIView.as_view() ),
    
    
    path('login', TokenObtainPairView.as_view() , name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh')
    
]