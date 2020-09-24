from django.urls import path
from . import views

app_name = 'achievement'

urlpatterns = [
    path('<int:theme_pk>', views.astore_list),
    path('theme_clear', views.theme_clear),
    path('theme_create/<int:theme_pk>',views.theme_create),
    path('visited/<int:theme_pk>', views.visited),

]