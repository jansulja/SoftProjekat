import imageProcessingFunctions as img_fun
import cv2
import numpy as np
import collections

def select_note_heads(image_orig, image_bin, groups):

    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dicts = [dict() for x in range(len(groups))]


    regions_dict = {}
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)

        #if w>10 and w<20:
        #if w>12 and w < 18 and h<23 and h>18:

        region = image_bin[y:y+h+1,x:x+w+1];
        row = find_row(groups,y)

        #print str(x) + "," + str(y) + ", row: " + str(row)


        dicts[row][x] = [img_fun.resize_region(region),(x,y,w,h)]

        regions_dict[x] = [img_fun.resize_region(region), (x,y,w,h)]
        cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)

    #sorted_regions_all_lines = get_sorted_regions(dicts)



    #sorted_regions_dict = collections.OrderedDict(sorted(regions_dict.items()))
    #sorted_regions = np.array(sorted_regions_dict.values())

    sorted_regions = get_sorted_regions(dicts)

    region_positions = []

    for x, y, w, h in sorted_regions[0:, 1]:
        region_positions.append(y)
    return image_orig, sorted_regions[:, 0], region_positions

def get_sorted_regions(dicts):

    sorted_dicts = [{}]*len(dicts)

    sorted_regions = []

    for i in range(len(dicts)):
        sorted_dicts.insert(0,collections.OrderedDict(sorted(dicts[i].items())))


    for i in range(len(sorted_dicts)):
        sorted_regions += sorted_dicts[i].values()

    return np.array(sorted_regions)


def find_row(groups,y):
    row =0
    for i in range(len(groups)):
        if y<groups[i][0] and y>groups[i][len(groups[i])-1]:
            row = i

    return row

def get_note_positions(image,groups):



    image_gray = img_fun.image_gray(image)
    image_bin = img_fun.image_bin(image_gray)
    image_bin = img_fun.invert(image_bin)

    image_bin = cv2.dilate(image_bin, np.ones((6,2)), iterations=1)
    verticalSize = 4;
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (verticalSize,1));

    image_bin = cv2.erode(image_bin, verticalStructure, iterations=1)
    image_bin = cv2.erode(image_bin, np.ones((7,1)), iterations=1)
    #image_bin = cv2.dilate(image_bin, np.ones((6,2)), iterations=1)
    #image_bin = img_fun.erode(image_bin)



    #image_bin = disconnect_note_heads(image.copy(), image_bin)

    # image_bin = cv2.erode(image_bin, verticalStructure, iterations=1)
    # image_bin = cv2.erode(image_bin, verticalStructure, iterations=3)

    # image_bin = disconnect_note_heads(image.copy(), image_bin)
    #
    # image_bin = cv2.erode(image_bin, np.ones((2,2)), iterations=1)
    # image_bin = img_fun.dilate(image_bin)



    # kernel = np.ones((3,3)) # strukturni element 3x3 blok
    #
    # image_bin = img_fun.dilate(image_bin)
    # #image_bin = img_fun.dilate(image_bin)
    #
    # kernel_vet = np.ones((6,1))
    # kernel_hor = np.ones((1,5))
    # image_bin = cv2.erode(image_bin, kernel_hor, iterations=1)
    # image_bin = cv2.dilate(image_bin, kernel_vet, iterations=1)
    #
    # image_bin = cv2.dilate(image_bin, kernel, iterations=1)
    # #image_bin = cv2.erode(image_bin, kernel, iterations=1)

    cv2.imshow('preparet image', image_bin)

    image_orig,selected_regions, positions = select_note_heads(image.copy(), image_bin, groups)



    cv2.imshow('asd', image_orig)

    return positions

def disconnect_note_heads(image, image_bin):
    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions_dict = {}
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)

        if w>25 and h>20:

            region = image_bin[y:y+h+1,x:x+w+1]
            region[:, w/2-2:w/2+2] = 0

            image_bin[y:y+h+1,x:x+w+1] = region


    return image_bin