from django.urls import path
from . import views

urlpatterns = [
    path('phonetoken/', views.phone_auth),
    path('<str:phone_num>/', views.phone),
]