from django.shortcuts import render
from .models import Image

def image_view(request):

	obj = Image.objects.get(id=1)

	context = {

		'obj':obj,

	}

	return render(request,'image/show.html',context)
