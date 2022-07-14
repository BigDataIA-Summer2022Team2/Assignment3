import keras
import numpy as np
from keras.models import load_model
import numpy as np
import os
from keras.applications.inception_v3 import preprocess_input

STATUS = ["Def", "Ok"]

abs_path = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
model_path = abs_path+"\\trained_model.h5"
model = load_model(model_path)

model.compile(optimizer="adam",loss='binary_crossentropy',metrics=['accuracy'])

img = keras.utils.load_img(abs_path + '\\src\\api_functions\\cast_def_0_148.jpeg', target_size = (256, 256))
img = keras.utils.img_to_array(img)
img = np.expand_dims(img,axis=0)
img = preprocess_input(img)

prediction = model.predict(img)
# print(prediction[0][0])

x = (prediction > 0.5).astype("int32")
print(STATUS[x[0][0]])
