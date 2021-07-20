from django.db import models
from django.db.models.fields import AutoField

class MyImage(models.Model):
	id = models.AutoField(primary_key=True)
	model_pic = models.ImageField(upload_to = '', default='')