from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from wineapi.views import UserViewSet, StyleViewSet, WineViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'styles', StyleViewSet, 'style')
router.register(r'wines', WineViewSet, 'wine')


urlpatterns = [
    path('', include(router.urls)),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
]

