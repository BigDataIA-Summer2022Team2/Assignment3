import base64
def imgToBase64(img):
    image_base64 = str(base64.b64encode(img), encoding='utf-8')
    return image_base64

def base64ToImg(img_base64):
    img_data = base64.b64decode(img_base64)
    return img_data
    
    