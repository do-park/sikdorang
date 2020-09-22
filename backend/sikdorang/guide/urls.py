from django.urls import path
from . import views

app_name = 'guide'

urlpatterns = [
    path('apply', views.apply_guide),
    path('list/<str:username>', views.list_guide),
    path('paid/<int:trip_pk>', views.paid),
    path('paidtour', views.paidtour),
    # path('guidetour/<int:tour_pk>', views.guidetour),
]