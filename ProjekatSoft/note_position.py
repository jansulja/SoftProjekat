import cv2
import numpy as np
import matplotlib.pyplot as plt
import imageProcessingFunctions as img_fun
import collections
import note_head_position
import note as nt
import soundGenerator as sgen

image = cv2.imread("images/sheet6.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


ret, image_bin = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

image_bin=img_fun.invert(image_bin)

horizontalsize = 200;
horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1));

image_bin = cv2.erode(image_bin, horizontalStructure, iterations=1)
image_bin = cv2.dilate(image_bin,horizontalStructure, iterations=1)



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

image_orig, selected_regions, lines = select_horizontal_lines(image.copy(), image_bin)
positions = note_head_position.get_note_positions(image)


print positions

cv2.imshow('binary', image)
cv2.waitKey(0)

def generate_notes(lines, note_positions):
    notes = []
    for note_y in note_positions:
        for i in range(0, len(lines)-1):
            if note_y < lines[i] and note_y > lines[i+1]:

                notes.append(get_note(i,note_y,lines[i]))
    return notes


def get_note(i,note_y,line_y):

    if i==0:
        if line_y-note_y < 5:
            return nt.Note('D4')
        else:
            return nt.Note('E4')
    elif i==1:

        if line_y-note_y < 5:
            return nt.Note('F4')
        else:
            return nt.Note('G4')
    elif i==2:
        if line_y-note_y < 5:
            return nt.Note('A4')
        else:
            return nt.Note('H4')
    elif i==3:
        if line_y-note_y < 5:
            return nt.Note('C5')
        else:
            return nt.Note('D5')


notes = generate_notes(lines, positions)

for i in range(len(notes)):
    notes[i].print_note()
    sgen.playNote(notes[i].frequency, notes[i].duration)



