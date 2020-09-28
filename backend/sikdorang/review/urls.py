from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('create_review/<int:store_pk>', views.create_review),
    path('user_review', views.user_review),
    path('store_review/<int:store_pk>', views.store_review),
    # path('review_chk/<int:store_pk>', views.review_chk),

]