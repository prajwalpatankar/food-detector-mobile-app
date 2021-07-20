from rest_framework import serializers
from rest_framework.serializers import (
      ModelSerializer,
)
from .models import MyImage

class imageSerializer(ModelSerializer):
   class Meta:
      model = MyImage
      fields = [
         'id',
         'model_pic'        
      ]
