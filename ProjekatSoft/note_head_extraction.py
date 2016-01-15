import imageProcessingFunctions as img_fun
import cv2
import numpy as np
import collections

image = img_fun.load_image('images/sheet4.png')
image_gray = img_fun.image_gray(image)
image_bin = img_fun.image_bin(image_gray)
image_bin = img_fun.invert(image_bin)


verticalSize = 3;
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (verticalSize,1));

image_bin = cv2.erode(image_bin, verticalStructure, iterations=1)

kernel = np.ones((3,3)) # strukturni element 3x3 blok

image_bin = img_fun.dilate(image_bin)
image_bin = img_fun.dilate(image_bin)
image_bin = cv2.dilate(image_bin, kernel, iterations=1)


cv2.imshow('binary', image_bin)
cv2.waitKey(0)



def select_note_heads(image_orig, image_bin):

    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions_dict = {}
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)

        #if w>10 and w<20:
        if w>16 and w < 23 and h<19:
            print str(w) + ',' + str(h)
            region = image_bin[y:y+h+1,x:x+w+1];
            regions_dict[x] = [img_fun.resize_region(region), (x,y,w,h)]
            cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)

    sorted_regions_dict = collections.OrderedDict(sorted(regions_dict.items()))
    sorted_regions = np.array(sorted_regions_dict.values())



    region_positions = []

    for x, y, w, h in sorted_regions[0:, 1]:
        region_positions.append((x,y))
    return image_orig, sorted_regions[:, 0], region_positions

image_orig,selected_regions, positions = select_note_heads(image.copy(), image_bin)

print positions

cv2.imshow('binary', image_orig)
cv2.waitKey(0)
