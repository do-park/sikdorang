from django.urls import path
from . import views

app_name = 'achievement'

urlpatterns = [
    path('<int:theme_pk>', views.astore_list),
]