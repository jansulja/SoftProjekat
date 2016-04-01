import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.dia import dia_matrix

import imageProcessingFunctions as img_fun
import collections
import note_head_position
import note as nt
import soundGenerator as sgen
import chord_head_positions as chp


def select_horizontal_lines(image_orig, image_bin):

    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    region_positions = []
    regions_dict = {}
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        region_positions.append(y)
        region = image_bin[y:y+h+1,x:x+w+1]
        regions_dict[x] = [img_fun.resize_region(region), (y, x, w, h)]
        cv2.rectangle(image_orig, (x, y), (x+w, y+h), (0, 255, 0), 2)

    sorted_regions_dict = collections.OrderedDict(sorted(regions_dict.items()))
    sorted_regions = np.array(sorted_regions_dict.values())


    return image_orig, sorted_regions[:, 0], region_positions

def generate_notes(lines, note_positions):

    notes = []

    for note_y in note_positions:
        for i in range(0, len(lines)-1):
            if note_y < lines[i] and note_y > lines[i+1]:

                notes.append(get_note(i%9,note_y,lines[i]))
    return notes


def get_note(i,note_y,line_y):

    if i==0:
        if line_y-note_y < 5:
            return nt.Note('G3')
        else:
            return nt.Note('A3')
    elif i==1:

        if line_y-note_y < 5:
            return nt.Note('H3')
        else:
            return nt.Note('C4')
    elif i==2:
        if line_y-note_y < 5:
            return nt.Note('D4')
        else:
            return nt.Note('E4')
    elif i==3:
        if line_y-note_y < 5:
            return nt.Note('F4')
        else:
            return nt.Note('G4')
    elif i==4:
        if line_y-note_y < 5:
            return nt.Note('A4')
        else:
            return nt.Note('H4')
    elif i==5:
        if line_y-note_y < 5:
            return nt.Note('C5')
        else:
            return nt.Note('D5')
    elif i==6:
        if line_y-note_y < 5:
            return nt.Note('E5')
        else:
            return nt.Note('F5')
    elif i==7:
        if line_y-note_y < 5:
            return nt.Note('G5')
        else:
            return nt.Note('A5')
    elif i==8:
        if line_y-note_y < 5:
            return nt.Note('H5')
        else:
            return nt.Note('C6')


def get_notes(image):


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    ret, image_bin = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    image_bin=img_fun.invert(image_bin)

    horizontalsize = 200;
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1));

    image_bin = cv2.erode(image_bin, horizontalStructure, iterations=1)
    image_bin = cv2.dilate(image_bin,horizontalStructure, iterations=1)

    image_orig, selected_regions, lines = select_horizontal_lines(image.copy(), image_bin)

    #cv2.imshow('lines', image_orig)

    lines,groups = add_additional_lines(lines)

    sheet = chp.get_note_positions(image,groups)

    notes = []
    #notes = generate_notes(lines, positions)

    return sheet

def get_average_line_distance(lines):

    distances = []
    for i in range(4):
        distances.append(lines[i]-lines[i+1])

    return sum(distances)/4

def add_additional_lines(lines):
    groups = []
    all_lines = []
    g=[]
    for i in range(len(lines)):
        g.append(lines[i])
        if len(g) == 5:
            groups.append(g)
            g =[]

    for i in range(len(groups)):
        groups[i].insert(0,groups[i][0]+get_average_line_distance(groups[i]))
        groups[i].insert(0,groups[i][0]+get_average_line_distance(groups[i]))
        groups[i].append(groups[i][len(groups[i])-1]-get_average_line_distance(groups[i]))
        groups[i].append(groups[i][len(groups[i])-1]-get_average_line_distance(groups[i]))


    for i in range(len(groups)):
        for j in range(len(groups[i])):
            all_lines.append(groups[i][j])

    return all_lines,groups