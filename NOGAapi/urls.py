from django.urls import path
from .views import RrgisterAPIView

urlpatterns = [
    path('register' , RrgisterAPIView.as_view())
]