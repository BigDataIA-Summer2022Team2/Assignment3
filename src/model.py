import numpy as np
import pandas as pd
import pickle
import keras,os
from keras.layers import Conv2D, MaxPool2D,Dropout,Flatten,Dense
from keras.preprocessing import image 
from keras.models import Sequential
from keras.applications import Xception


train_data_gen = image.ImageDataGenerator(rescale= 1./255)
train= train_data_gen.flow_from_directory(directory="./src/train", target_size=(256,256) , batch_size=32, class_mode = 'binary')
train.class_indices



xcept = Xception(input_shape = (256, 256, 3), include_top = False, weights = 'imagenet')

for layer in xcept.layers:
    layer.trainable = False


model=keras.Sequential([
    xcept,
    keras.layers.Flatten(),
    keras.layers.Dense(units=256, activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(units=1, activation="sigmoid"),
])

model.compile(optimizer="adam",loss='binary_crossentropy',metrics=['accuracy'])

model.summary()

len(train)/32

model.fit_generator(train,epochs=10,steps_per_epoch=7)

with open('model_pkl', 'wb') as files:
    pickle.dump(model, files)

#pickle.load(open("model_pkl","rb"))

