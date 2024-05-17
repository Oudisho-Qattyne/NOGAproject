from django.urls import path
from .views import RrgisterAPIView , UsersApiView , UserApiView , BranchsAPIView , BranchAPIView , CityAPIView , CitiesAPIView

urlpatterns = [
    path('register' , RrgisterAPIView.as_view()),
    path('users' , UsersApiView.as_view() ),
    path('users/<int:pk>' , UserApiView.as_view() ),
    path('branchs' , BranchsAPIView.as_view() ),
    path('branchs/<int:pk>' , BranchAPIView.as_view() ),
    path('cities' , CitiesAPIView.as_view() ),
    path('cities/<int:pk>' , CityAPIView.as_view() ),
]