from django.urls import path
from .views import RrgisterAPIView , UsersApiView , UserApiView , EmployeesApiView , EmployeeApiView , Job_TypesView , Job_TypeView , BranchsAPIView , BranchAPIView , CitiesAPIView , CityAPIView

urlpatterns = [
    path('register' , RrgisterAPIView.as_view()),
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
]