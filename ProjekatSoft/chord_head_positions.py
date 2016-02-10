import imageProcessingFunctions as img_fun
import cv2
import numpy as np
import collections
from matplotlib import pyplot as plt
import region as reg
import Regions as regs
import sheet as sh
import player as pl


def find_row(groups,y):
    row =0
    for i in range(len(groups)):
        if y<groups[i][0] and y>groups[i][len(groups[i])-1]:
            row = i

    return row

def disconnect_note_heads(image, image_bin):
    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions_dict = {}
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w>20 and h>13:
            region = image_bin[y:y+h+1,x:x+w+1]
            region[:, w/2-2:w/2+2] = 0
            image_bin[y:y+h+1,x:x+w+1] = region
    return image_bin

def select_note_heads_quarter(image_orig, image_bin, groups, dicts,regions):
    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions_dict = {}
    for contour in contours:

        x,y,w,h = cv2.boundingRect(contour)
        if w >8 and w<15 and h>7 and h<12:
            region = image_bin[y:y+h+1,x:x+w+1];
            regions_dict[x] = [img_fun.resize_region(region), (x,y,w,h)]
            cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)
            row = find_row(groups,y)
            dicts[row][x] = [img_fun.resize_region(region),(x,y,w,h)]
            r = reg.Region(x,y,w,h)
            regions.add_region(r)

    return image_orig,dicts,regions

def select_note_heads_half(image_orig, image_bin, groups, dicts,regions):

    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    regions_dict = {}
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        (x,y),(w,h),angle = rect
        if angle < -20 and angle>-50:
            x,y,w,h = cv2.boundingRect(contour)
            region = image_bin[y:y+h+1,x:x+w+1];
            regions_dict[x] = [img_fun.resize_region(region), (x,y,w,h)]
            cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)
            row = find_row(groups,y)
            dicts[row][x] = [img_fun.resize_region(region),(x,y,w,h)]
            r = reg.Region(x,y,w,h)
            regions.add_region(r)
    return image_orig,dicts,regions


def select_note_heads_whole(image_orig, image_bin, groups,dicts,regions):

    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    regions_dict = {}
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        (x,y),(w,h),angle = rect
        #if angle < -40 and angle > -50 and w > 6 and w<8 and h > 5:
        if w<8 and w > 4  and h> 9 and angle > -1:
            print '////////////////'
            print w,h,angle
            x,y,w,h = cv2.boundingRect(contour)
            region = image_bin[y:y+h+1,x:x+w+1];
            regions_dict[x] = [img_fun.resize_region(region), (x,y,w,h)]
            cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)
            row = find_row(groups,y)
            dicts[row][x] = [img_fun.resize_region(region),(x,y,w,h)]
            r = reg.Region(x,y,w,h)
            regions.add_region(r)
    return image_orig,dicts,regions

def select_sharps(image_orig, image_bin, groups):

    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    regions = regs.Regions(groups)
    regions_dict = {}
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w<8 and w>4 and h<7 and h>2:
            region = image_bin[y:y+h+1,x:x+w+1];
            cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)
            r = reg.Region(x,y,w,h)
            regions.add_region(r)
    return image_orig,regions

def select_bar_lines(image_orig, image_bin, groups):

    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    regions = regs.Regions(groups)
    regions_dict = {}
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w<3:
            region = image_bin[y:y+h+1,x:x+w+1];
            cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)
            r = reg.Region(x,y,w,h)
            regions.add_region(r)
    return image_orig,regions

def prepare_quarter_notes(image):
    image_gray = img_fun.image_gray(image)
    image_bin = img_fun.image_bin(image_gray)
    image_bin = img_fun.invert(image_bin)
    verticalSize = 3;
    horSize = 3
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (verticalSize,1));
    horStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1,horSize));
    image_bin = cv2.erode(image_bin, verticalStructure, iterations=1)
    image_bin = cv2.morphologyEx(image_bin, cv2.MORPH_OPEN, np.ones((5,5)))
    image_bin = disconnect_note_heads(image.copy(),image_bin)
    return image_bin

def prepare_half_notes(image):
    image_gray = img_fun.image_gray(image)
    image_bin = img_fun.image_bin(image_gray)
    image_bin = cv2.morphologyEx(image_bin, cv2.MORPH_OPEN, np.ones((4,4)))
    image_bin = cv2.erode(image_bin,np.ones((2,2)),iterations=1)
    image_bin = img_fun.invert(image_bin)
    return  image_bin

def prepare_whole_notes(image):
    image_gray = img_fun.image_gray(image)
    image_bin = img_fun.image_bin(image_gray)
    image_bin = cv2.erode(image_bin,np.ones((1,2)),iterations=3)
    image_bin = img_fun.invert(image_bin)

    cv2.imshow('aaaaaaaaaaaa',image_bin)

    return image_bin

def prepare_sharps(image):

    image_gray = img_fun.image_gray(image)
    image_bin = img_fun.image_bin(image_gray)
    image_bin = img_fun.invert(image_bin)

    image_bin = cv2.erode(image_bin,np.ones((1,3)),iterations=1)

def prepare_sharps(image):

    image_gray = img_fun.image_gray(image)
    image_bin = img_fun.image_bin(image_gray)
    image_bin = img_fun.invert(image_bin)

    image_bin = cv2.erode(image_bin,np.ones((1,3)),iterations=1)

    cv2.imshow('acc',image_bin)
    return image_bin

def prepare_bar_lines(image):

    image_gray = img_fun.image_gray(image)
    image_bin = img_fun.image_bin(image_gray)
    image_bin = img_fun.invert(image_bin)



    cv2.imshow('bar lines',image_bin)
    return image_bin

def get_sorted_regions(dicts):
    sorted_dicts = [{}]*len(dicts)
    sorted_regions = []
    for i in range(len(dicts)):
        sorted_dicts.insert(0,collections.OrderedDict(sorted(dicts[i].items())))

    for i in range(len(sorted_dicts)):
        sorted_regions += sorted_dicts[i].values()

    return np.array(sorted_regions)

def get_note_positions(image,groups):
    dicts = [dict([]) for x in range(len(groups))]

    regions = regs.Regions(groups)

    # print dicts
    image_bin = prepare_quarter_notes(image.copy())
    image_q,dicts,regions = select_note_heads_quarter(image.copy(),image_bin,groups,dicts,regions)
    image_bin = prepare_half_notes(image.copy())
    image_h,dicts,regions = select_note_heads_half(image.copy(),image_bin,groups,dicts,regions)
    image_bin = prepare_whole_notes(image.copy())
    image_w,dicts,regions = select_note_heads_whole(image.copy(),image_bin,groups,dicts,regions)

    image_bin_acc = prepare_sharps(image.copy())
    image_sh,reg_sharps = select_sharps(image.copy(),image_bin_acc,groups)
    sorted_acc = reg_sharps.get_sorted_regions()

    image_bin_bar_lines = prepare_bar_lines(image.copy())
    image_bar_ln,reg_bar_lines = select_bar_lines(image.copy(),image_bin_bar_lines,groups)
    sorted_bar_lines = reg_bar_lines.get_sorted_regions()


    cv2.imshow('sharp regs',image_sh)




    sorted = regions.get_sorted_regions()

    sheet = sh.Sheet(sorted,groups,sorted_bar_lines,sorted_acc)

    cv2.imshow('quarter',image_q)
    cv2.imshow('half',image_h)
    cv2.imshow('whole',image_w)
    #
    # player = pl.Player(sheet)
    # player.play_sheet()

    return sheet



    # sorted_regions = get_sorted_regions(dicts)
    # region_positions = []
    # for x, y, w, h in sorted_regions[0:, 1]:
    #     region_positions.append(y)
    #
    # return region_positions
