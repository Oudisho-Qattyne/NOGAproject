from django.urls import path
from .views import *

urlpatterns = [
    path('register' , RrgisterAPIView.as_view()),
    path('users' , UsersApiView.as_view() ),
    path('users/<int:pk>' , UserApiView.as_view() ),
    path('Emp',EmployeesApiView.as_view()),
    path('JobT',Job_TypeView.as_view())
]