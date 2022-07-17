import keras
import numpy as np
from keras.models import load_model
import numpy as np
import os
from keras.applications.inception_v3 import preprocess_input
from PIL import Image
import io
import pickle

#import tflearn
def qualityinspection(file):
    STATUS = ["Defect", "Ok"]
    #model = joblib.load('./model.pkl')
    abs_path = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
    model_path = abs_path+"/trained_model.h5"
    # with open('model_pkl', 'rb') as file:  
    #     model = pickle.load(file)
    #model = pickle.load(open(model_path, 'rb'))
    #pickle.load(open(model_path, 'rb'))
    model = load_model(model_path)
    model.compile(optimizer="adam",loss='binary_crossentropy',metrics=['accuracy'])

    #img = keras.utils.load_img(abs_path + '\\src\\api_functions\\cast_def_0_148.jpeg', target_size = (256, 256))
    # img = keras.utils.load_img(file, target_size = (256, 256))
    # img = keras.utils.img_to_array(img)
    # img = np.expand_dims(img,axis=0)
    # img = preprocess_input(img)

    img = Image.open(io.BytesIO(file))
    img = img.convert('RGB')
    img = img.resize((256, 256), Image.NEAREST)
    img = keras.utils.img_to_array(img)
    img = np.expand_dims(img,axis=0)
    img = preprocess_input(img)
    prediction = model.predict(img)
    # print(prediction[0][0])

    x = (prediction > 0.5).astype("int32")
    response = {}
    #response["image name"] = filename
    response["status"] = STATUS[x[0][0]]
    response["probability"] = str(round(prediction[0][0] * 100,3)) + "%"
    return response
