"""register api urls """
from rest_framework import routers
from django.urls import path, include
from todo.apis.views import TodoModelViewSet, NotificationViewSet
router = routers.DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename='notifications')
router.register(r"", TodoModelViewSet, basename='todo')


urlpatterns = [
    path("", include(router.urls))
]
