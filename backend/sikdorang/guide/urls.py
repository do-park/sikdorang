from django.urls import path
from . import views

app_name = 'guide'

urlpatterns = [
    path('apply', views.apply_guide),
    path('list/<str:username>', views.list_guide),
]