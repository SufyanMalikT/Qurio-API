"""
URL configuration for Qurio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework import routers
from app.views import CustomUserViewSet, QuestionsViewSet, AnswerViewSet, TagViewSet, CookieTokenRefreshView,CookieTokenObtainView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'users',CustomUserViewSet,basename='users')
router.register(r'questions',QuestionsViewSet,basename='questions')
router.register(r'answers',AnswerViewSet,basename='answers')
router.register(r'tags',TagViewSet,basename='tags')

nested_router = NestedDefaultRouter(router,'questions',lookup='questions')
nested_router.register(r'answers',AnswerViewSet,basename='answers')
nested_router.register(r'tags',TagViewSet,basename='tags')

nested_router2 = NestedDefaultRouter(router,'tags',lookup='tags')
nested_router2.register(r'questions',QuestionsViewSet,basename='questions')

router_urls = router.urls + nested_router.urls + nested_router2.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router_urls)),

    path('api/auth/login/',CookieTokenObtainView.as_view(),name='obtain-token'),
    path('api/token/refresh/',CookieTokenRefreshView.as_view(),name='token-refresh')
]
