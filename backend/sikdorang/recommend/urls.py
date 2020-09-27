from django.urls import path
from . import views

app_name = 'recommend'

urlpatterns = [
    path('<int:user_pk>', views.recommend),
    path('tag-recommend/', views.get_tag_recommendation),
    path('coldstart', views.coldstart),
]