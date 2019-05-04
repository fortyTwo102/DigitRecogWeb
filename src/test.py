import pandas as pd
import numpy as np
import csv,cv2

def insert_row(idx, df, df_insert):
    return df.iloc[:idx, ].append(df_insert).append(df.iloc[idx:, ]).reset_index(drop = True)

train = pd.read_csv("X_train.csv",index_col=0)

filename = str(train.shape[0]) + ".png"

index = train.shape[0]

img = cv2.imread(filename,0)

resized = cv2.resize(img, (28,28), interpolation = cv2.INTER_AREA)

p = pd.DataFrame(resized.reshape(1,-1))






train = pd.concat([train[:49000], p.rename(columns=dict(zip(p.columns,train.columns))), train[49000:]])

'''with open("X_train.csv","a+",newline="",encoding="utf-8") as f:
	csv_writer = csv.writer(f)

	csv_writer.writerows([p])'''
