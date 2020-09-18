from django.urls import path
from . import views

app_name = 'recommend'

urlpatterns = [
    path('<int:user_pk>', views.recommend),
]