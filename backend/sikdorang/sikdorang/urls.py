"""sikdorang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from django.conf.urls.static import static
from sikdorang import settings
from trip.views import TripViewSet
from review.views import ReviewViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="식도랑 프로젝트",
      default_version='v1',
      description="플라잉승희호에는 선장이 필요하다",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="고잉승희호"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('trip', TripViewSet) # prefix = movies , viewset = MovieViewSet
router.register('review', ReviewViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # 로그인 & 로그아웃
    url(r'^rest-auth/', include('rest_auth.urls')),
    # 소셜 로그인
    url(r'^accounts/', include('allauth.urls')),
    # 회원가입
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # 여행
    path('trip/', include('trip.urls')),
    path('review/', include('review.urls')),
    path('achievement/', include('achievement.urls')),
    # 추천
    path('recommend/', include('recommend.urls')),
    url(r'^',include(router.urls)),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
