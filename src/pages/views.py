from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from PIL import Image
import cv2,csv,os
import pandas as pd
from django.core.files.storage import default_storage
import pickle
import sklearn.model_selection
from training.models import Training
from sklearn.neural_network import MLPClassifier

from trydjango import settings

# Create your views here.

global data

def home_view(request):

	return render(request,'home.html',{})

def trainModel():

	offset = 3

	size = Training.objects.count()

	print("size: ",size)

	train = []

	for i in range(size):

		data_point = Training.objects.get(id=i+offset)
		
		train.append(data_point.data)
		

	train = pd.DataFrame(train)	

	print("train: ",train)

	X_train =  train.iloc[:,:-1]
	y_train =  train.iloc[:,-1]

	X_train = X_train / 255.0

	print(X_train.shape, y_train.shape)

	model = MLPClassifier(hidden_layer_sizes=(50,), max_iter=100, alpha=1e-4,
                    solver='sgd', tol=1e-4, random_state=1,
                    learning_rate_init=.1,verbose=True)

	model.fit(X_train,y_train)

	modelpath = os.path.join(settings.BASE_DIR, "static") + '\\MLPClassifier.pkl'

	with open(modelpath,'wb') as f:
		print("Saving the model. . . ")
		pickle.dump(model,f)

	return model


'''	
	pickle_filename = 'MLPClassifier.pkl'

	with open(pickle_filename,'wb') as f:
		pickle.dump(model,f)'''



	#return model

def addToDatabase(p):

	i = int(Training.objects.count()) 
			
	newData = Training.objects.create(index=i, data=list(p))
	newData.save()
			
	print("added index: ",i)

def predictDraw(p):

	p = p.reshape(1,-1)
						
	p = 255 - p

	p = p / 255.0

	modelpath = os.path.join(settings.BASE_DIR, "static") + '\\MLPClassifier.pkl'

	exists = os.path.isfile(modelpath)

	if exists:
		with open(modelpath,"rb") as f:
			model = pickle.load(f)
	else:
		print("Model isn't saved.")
		model = trainModel()		

	print(model.predict(p))



def predictFile(filepath):

	print("filepath: ",filepath)

	img = cv2.imread(filepath,0)

	res = cv2.resize(img, (28,28), interpolation = cv2.INTER_AREA)

	p = res.reshape(1,-1)

	p = 255 - p

	p = p / 255.0

	modelpath = os.path.join(settings.BASE_DIR, "static") + '\\MLPClassifier.pkl'


	exists = os.path.isfile(modelpath)

	if exists:
		with open(modelpath,"rb") as f:
			model = pickle.load(f)
	else:
		print("Model isn't saved.")
		model = trainModel()		


	print(model.predict(p))

@csrf_exempt
def draw_view(request):

	global data

	data = request.body

	if len(data) > 0:

		filepath = os.path.join(settings.BASE_DIR, "static") + "\\file.png"
		

		img = np.frombuffer(data, dtype=np.uint8).reshape((300, 300, 4))

		cv2.imwrite(filepath,img)

		img_gray = 255 - img[:, :, 3]

		resized = cv2.resize(img_gray, (28,28), interpolation = cv2.INTER_AREA)

		#predictDraw(resized)



		'''user_inputs = []
									found = False
									for file in os.listdir(default_storage.location):
										
										if file.endswith(".png"):
											found = True
											user_inputs.append(int(file[:-4]))
							
							
									
							
									
									
									if not found:
										filepath = default_storage.location+"\\1.png"
										cv2.imwrite(filepath,resized)
										predictFile(filepath)
							
							
									else:
										
										filename = max(user_inputs)+1
										
										filename = str(filename) + ".png"
										
										filepath = default_storage.location+"\\"+filename
										
										cv2.imwrite(filepath,resized)'''

		
		

		#predictFile(filepath)



				

	context = {}
	

	return render(request,'draw.html',context)	

@csrf_exempt
def predict_view(request):


	print("Predicting.... ")

	if len(data) > 0:

		img = np.frombuffer(data, dtype=np.uint8).reshape((300, 300, 4))

		img_gray = 255 - img[:, :, 3]

		resized = cv2.resize(img_gray, (28,28), interpolation = cv2.INTER_AREA)

		predictDraw(resized)

	filepath = os.path.join(settings.BASE_DIR, "static") + "\\file.png"
		
	#img = cv2.imread(filepath,0) 
		
	context = {
		"img" : filepath
	}

	return render(request,'predict.html',context)	