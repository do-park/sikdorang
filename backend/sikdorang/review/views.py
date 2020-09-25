from rest_framework import viewsets
from .serializers import *
from .models import Review
# Create your views here.

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer