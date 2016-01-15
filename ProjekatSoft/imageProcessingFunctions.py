import cv2
import numpy as np
import matplotlib.pyplot as plt
import collections


def resize_region(region):
    return cv2.resize(region, (28, 28), interpolation=cv2.INTER_NEAREST)


def invert(image):
    return 255-image


def select_roi(image_orig, image_bin):

    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions_dict = {}
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)

        #if w>10 and w<20:
        if w>13:
            print str(w) + ',' + str(h)
            region = image_bin[y:y+h+1,x:x+w+1];
            regions_dict[x] = [resize_region(region), (x,y,w,h)]
            cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)

    sorted_regions_dict = collections.OrderedDict(sorted(regions_dict.items()))
    sorted_regions = np.array(sorted_regions_dict.values())



    region_positions = []

    for x, y, w, h in sorted_regions[1:-1, 1]:
        region_positions.append(y)


    return image_orig, sorted_regions[:, 0], region_positions

def display_progress(data, centers, labels):

    colors = iter(plt.cm.gist_rainbow(np.linspace(0,1,len(centers))))
    for idx, center in enumerate(centers):
        center_group = data[np.where(labels == idx)]
        color = next(colors)
        plt.scatter(center_group[:,0],center_group[:,1], c=color, marker='o', s=50)
        plt.scatter(center[0],center[1], c=color, marker='x', s=200)
    plt.show()


def load_image(path):
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)


def image_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def image_bin(image_gs):
    ret,image_bin = cv2.threshold(image_gs, 127, 255, cv2.THRESH_BINARY)
    return image_bin


def invert(image):
    return 255-image


def display_image(image, color= False):
    if color:
        plt.imshow(image)
    else:
        plt.imshow(image, 'gray')


def dilate(image):
    kernel = np.ones((3,3)) # strukturni element 3x3 blok
    return cv2.dilate(image, kernel, iterations=1)


def erode(image):
    kernel = np.ones((3,3)) # strukturni element 3x3 blok
    return cv2.erode(image, kernel, iterations=1)

