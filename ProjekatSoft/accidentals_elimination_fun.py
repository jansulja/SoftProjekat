import imageProcessingFunctions as img_fun
import numpy as np
import cv2
def eliminate(image,results,reg_details):

    for i in range(len(reg_details)):
        if results[i]== "acc":
            d = reg_details[i]
            x = d[0]
            y = d[1]
            w = d[2]
            h = d[3]
            image[y:y+h+1,x:x+w+1] = 255


    return image