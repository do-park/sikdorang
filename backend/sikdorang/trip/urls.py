from django.urls import path
from . import views

app_name = 'trip'

urlpatterns = [
    path('list/<int:user_pk>', views.trip_list),
    # path('create/', views.create_trip),
    # path('<int:trip_pk>', views.trip_detail),
]