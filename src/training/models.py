from django.db import models
from django_mysql.models import ListCharField

# Create your models here.

class Training(models.Model):
	index = models.IntegerField()
	data = ListCharField(
		base_field=models.IntegerField(),
		size = 800,
		max_length = 11*800
	)

