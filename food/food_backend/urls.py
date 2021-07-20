from django.conf.urls import include, url
from food_backend import views
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()
router.register(r'upload', views.ImageCreateAPIView)

urlpatterns = [
    path('ingredients',views.model_call, name = "ingredients"),
    path('', include(router.urls)),    
]