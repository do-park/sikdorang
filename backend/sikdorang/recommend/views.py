from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Store

@api_view(['GET'])
def get_tag_recommendation(request, user_pk):
    User = get_user_model()
    user = get_