from django.db import models
from django_mysql.models import ListCharField

# Create your models here.

class Image(models.Model):

	name = models.TextField()
	image = models.ImageField(upload_to='user_input')


