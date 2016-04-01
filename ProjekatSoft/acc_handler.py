import imageProcessingFunctions as img_fun
import cv2
import numpy as np
class Acc_handler:
    def __init__(self,image):
        self.image = image
        image_gray = img_fun.image_gray(image)
        ret, self.image_bin = cv2.threshold(image_gray, 150, 255, cv2.THRESH_BINARY)
        self.image_bin = img_fun.invert(self.image_bin)



        self.remove_accs()

    def remove_accs(self):

        image_orig = self.image.copy()
        img, contours, hierarchy = cv2.findContours(self.image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for contour in contours:

            x,y,w,h = cv2.boundingRect(contour)



            if w < 15 and h < 30 and w > 7 and h>23:
                region = self.image_bin[y:y+h+1,x:x+w+1]
                region = region*0
                self.image_bin[y:y+h+1,x:x+w+1] = region
                cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)

        return self.image_bin