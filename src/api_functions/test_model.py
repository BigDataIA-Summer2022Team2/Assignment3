import keras
import numpy as np
from keras.models import load_model
import numpy as np
import os
from keras.applications.inception_v3 import preprocess_input
from PIL import Image
import io
import boto3
from boto3 import client
from json import load
import json

def qualityinspection(file):
    STATUS = ["Defect", "Ok"]

    #Todo Load Transfer Learning model from Amason S3
    """
    when user wants to create a Docker container
    We can use params from user input to create a model.yaml file to store keys 
    """
    abs_path = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
    try:
        model_path = abs_path + '/src/trained_model.h5'
        model = load_model(model_path)
        model.compile(optimizer="adam",loss='binary_crossentropy',metrics=['accuracy'])
        
        img = Image.open(io.BytesIO(file))
        img = img.convert('RGB')
        img = img.resize((256, 256), Image.NEAREST)
        img = keras.utils.img_to_array(img)
        img = np.expand_dims(img,axis=0)
        img = preprocess_input(img)
        prediction = model.predict(img)

        x = (prediction > 0.5).astype("int32")
        response = {}
        #response["image name"] = filename
        response["status"] = STATUS[x[0][0]]
        response["probability"] = str(round(prediction[0][0] * 100,3)) + "%"
    except Exception as err:
        print(err)
        response = {"detail":""}
    return response

