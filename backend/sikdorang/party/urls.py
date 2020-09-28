from django.urls import path
from . import views

app_name = 'party'

urlpatterns = [
    path('create_party/<int:trip_pk>', views.create_party),
    path('list_party', views.list_party),
    path('detail_party/<int:party_pk>', views.detail_party),
    path('update_party/<int:party_pk>', views.update_party),
    path('delete/<int:party_pk>', views.delete_party),
    path('create_message/<int:party_pk>', views.create_message),
    path('list_message/<int:party_pk>', views.list_message),
]