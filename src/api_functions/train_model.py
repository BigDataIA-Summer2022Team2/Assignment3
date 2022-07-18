import numpy as np
import pandas as pd
import keras,os
from keras.layers import Conv2D, MaxPool2D,Dropout,Flatten,Dense
from keras.preprocessing import image 
from keras.models import Sequential
from keras.applications.inception_v3 import InceptionV3
import joblib
abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
        
train_path = abs_path+"/train"
test_path = abs_path+"/test"

train_data_gen = image.ImageDataGenerator(rescale= 1./255)
train= train_data_gen.flow_from_directory(directory=train_path, target_size=(256,256) , batch_size=32, class_mode = 'binary')

train_data_gen = image.ImageDataGenerator(rescale= 1./255)
test= train_data_gen.flow_from_directory(directory=test_path , target_size=(256,256) , batch_size=32, class_mode = 'binary')

inceptionv3 = InceptionV3(input_shape = (256, 256, 3), include_top = False, weights = 'imagenet')

for layer in inceptionv3.layers:
    layer.trainable = False


model=keras.Sequential([
    inceptionv3,
    keras.layers.Flatten(),
    keras.layers.Dense(units=256, activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(units=1, activation="sigmoid"),
])

model.compile(optimizer="adam",loss='binary_crossentropy',metrics=['accuracy'])

model.summary()

model.fit_generator(train,epochs=12,steps_per_epoch=30,validation_data=test,validation_steps=len(test))

joblib.dump(model, 'model.pkl')
# with open('model_pkl', 'wb') as files:
#      pickle.dump(model, files)
#model.save('trained_model.h5')

#pickle.load(open("model_pkl","rb"))

