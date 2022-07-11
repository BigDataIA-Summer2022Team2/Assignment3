import os
from PIL import Image
import numpy as np


def imgToPixel(img_name):
    current_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    img_path = current_dir + "\\" + img_name

    open_img = Image.open(img_path)
    
    img_data = np.asarray(open_img)
    #print(img_data.shape)

    return img_data


# current_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
# img_path = current_dir + "\\" + "0041e69431bf872309d1aff628b6494f.jpg"

# open_img = Image.open(img_path)
# img_data = np.asarray(open_img)
# print(img_data.shape) #(725, 1279, 3)
# print(img_data)

#     ###################
# img_ = Image.fromarray(img_data)
# img_.show()