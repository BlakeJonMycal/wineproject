from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from wineapi.views import register_user, login_user, StyleViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'styles', StyleViewSet, 'style')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user), 
    path('login', login_user), 
]

