import io as IO
import base64
import cv2
import os
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import tensorflow as tf 

model = tf.keras.models.load_model('resource/bg.h5')

def load_img(image_location):
    img = io.imread(image_location)
    img = cv2.resize(img[:,:,0:3], (256,256), interpolation=cv2.INTER_AREA)
    return img

def save_img(img,image_name, upload_folder):
    image_location = os.path.join(upload_folder, image_name)
    plt.imsave(image_location, img)
    return image_location

def bg_remove(imgpath=None, img=None, model=model):
    if imgpath:
        im = io.imread(imgpath)
    else:
        im = img.copy()
    
    im = cv2.resize(im[:,:,0:3],(256,256))
    
    img = np.array(im)/255
    img = img.reshape((1,)+img.shape)
    pred = model.predict(img)

    p = pred.copy()
    p = p.reshape(p.shape[1:-1])

    p[np.where(p>.25)] = 1
    p[np.where(p<.25)] = 0

    im[:,:,0] = im[:,:,0]*p 
    im[:,:,0][np.where(p!=1)] = 255
    im[:,:,1] = im[:,:,1]*p 
    im[:,:,1][np.where(p!=1)] = 255
    im[:,:,2] = im[:,:,2]*p
    im[:,:,2][np.where(p!=1)] = 255

    return im

def convert_into_base64(image):
    try:
        image = open(image, 'rb')
        image = image.read()
        return base64.b64encode(image)
    except  Exception as error:
        return error