from django.urls import path
from .views import RrgisterAPIView , UsersApiView , UserApiView

urlpatterns = [
    path('register' , RrgisterAPIView.as_view()),
    path('users' , UsersApiView.as_view() ),
    path('users/<int:pk>' , UserApiView.as_view() ),
]