import csv
import pandas as pd
import numpy as np
from training.models import Training

			
X_train = np.array(pd.read_csv("X_train.csv",index_col=0))
y_train = np.array(pd.read_csv("train.csv",index_col=0))

print(X_train.shape,y_train.shape)
a = np.array(X_train)
b = np.array(y_train)
c = np.column_stack((a,b))		
i=0



for each in c:
	p = Training.objects.create(index=i, data=list(each))
	p.save()
	print("added index",i)
	i=i+1