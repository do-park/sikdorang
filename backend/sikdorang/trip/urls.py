from django.urls import path
from . import views

app_name = 'trip'

urlpatterns = [
    path('list/<int:user_pk>', views.trip_list),
    path('chk/<str:name>', views.checkID),
    path('idealtag', views.idealtag),
    path('idealcategory', views.idealcategory),
    # path('create/', views.create_trip),
    # path('<int:trip_pk>', views.trip_detail),
]