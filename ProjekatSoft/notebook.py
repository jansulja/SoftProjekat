import imageProcessingFunctions as img_fun
import cv2
import collections
import numpy as np
import note_positions_fun as npt
import region as reg
import Regions as regs
import sheet as sh
import player as pl

class Notebook:
    def __init__(self,image):
        self.image = image
        self.select_lines()
        self.prepare_image()
        self.show_lines_and_notes()
        self.select_bar_lines()
        self.generate_sheet()

    def show_lines_and_notes(self):

        image = self.image.copy();

        for reg in self.note_regs.regions:
            cv2.rectangle(image, (reg.x, reg.y), (reg.x+reg.w, reg.y+reg.h), (255, 0, 0), 2)

        for reg in self.h_lines:
            cv2.rectangle(image, (reg.x, reg.y), (reg.x+reg.w, reg.y), (0, 255, 0), 2)

        img_fun.show_image('all',image)

    def generate_sheet(self):
        sheet = sh.Sheet(self.note_regs.get_sorted_regions(),self.groups,self.bar_lines_regs.get_sorted_regions(),[[] for i in range(len(self.groups))])
        player = pl.Player(sheet)
        player.play_sheet(sheet.get_all_chords(),"JR_organ.sf2")

    def prepare_bar_lines(self):
        image_gray = img_fun.image_gray(self.image.copy())
        image_bin = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 33, 5)

        image_bin = cv2.erode(image_bin,np.ones((3,3)),iterations=1)
        image_bin = cv2.dilate(image_bin,np.ones((3,20)),iterations=1)

        kernel = np.ones((12,12),np.uint8)
        image_bin = cv2.morphologyEx(image_bin, cv2.MORPH_OPEN, kernel)
        image_bin = cv2.dilate(image_bin,np.ones((20,1)),iterations=1)

        # horizontalsize = 50
        # horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1,horizontalsize))
        # image_bin = cv2.erode(image_bin, horizontalStructure, iterations=1)
        # image_bin = cv2.dilate(image_bin,horizontalStructure, iterations=1)

        # cv2.imshow('bar lines',image_bin)
        # cv2.waitKey(0)
        img_fun.show_image('bars',image_bin)
        return image_bin

    def select_bar_lines(self):
        image = self.image.copy()
        image_bin = self.prepare_bar_lines()
        img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        regions = regs.Regions(self.groups)
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)

            if w < 35 and h>100:

                r = reg.Region(x,y,w,h)
                regions.add_region(r)
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)


        # cv2.imshow('bar lines',image)
        img_fun.show_image('bars',image)
        self.bar_lines_regs = regions



    def prepare_image(self):


        self.image_gray = img_fun.image_gray(self.image)

        self.image_bin = cv2.adaptiveThreshold(self.image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 33, 5)
        image_bin =  self.image_bin

        image_bin = cv2.erode(image_bin,np.ones((3,3)),iterations=1)
        image_bin = cv2.dilate(image_bin,np.ones((3,20)),iterations=1)

        kernel = np.ones((12,12),np.uint8)
        image_bin = cv2.morphologyEx(image_bin, cv2.MORPH_OPEN, kernel)
        image_bin = cv2.erode(image_bin,np.ones((3,30)),iterations=1)


        img_fun.show_image('bars',image_bin)

        self.image_bin = image_bin
        self.select_regions(self.image.copy(),image_bin)







    def select_lines(self):
        image_gray = img_fun.image_gray(self.image)
        image_bin = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 33, 5)

        horizontalsize = 50
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))
        image_bin = cv2.erode(image_bin, horizontalStructure, iterations=1)
        image_bin = cv2.dilate(image_bin,horizontalStructure, iterations=1)

        # image_bin = cv2.dilate(image_bin,np.ones((2,500)), iterations=1)
        image_bin = cv2.dilate(image_bin,np.ones((2,200)), iterations=1)


        img,reg,pos = self.select_horizontal_lines(self.image.copy(),image_bin)

        lines,groups = npt.add_additional_lines(pos)

        self.lines = lines
        self.groups = groups

        # cv2.imshow('lines',cv2.resize(image_bin, (1000, 750), interpolation=cv2.INTER_NEAREST))
        # cv2.waitKey(0)
        # cv2.imshow('aaaaaaaaaa',img)

        img_fun.show_image('bin',image_bin)
        img_fun.show_image('img' ,img)

    def select_regions(self,image,image_bin):

        img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        regions = regs.Regions(self.groups)

        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)

            # if w>6 and w<19 and h > 11 and h < 27:
            #if w>6 and w<30and h > 11 and h < 40 and x > 250:
            if x > 250:
                print 'w,h',w,h
                r = reg.Region(x,y,w,h)
                regions.add_region(r)
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # cv2.imshow('lines',image)
        # cv2.waitKey(0)

        img_fun.show_image('regions',image)

        self.note_regs = regions


    def select_horizontal_lines(self,image_orig, image_bin):

        regions = []

        img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        region_positions = []
        regions_dict = {}
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            if w>1000:
                r = reg.Region(x,y,w,h)
                regions.append(r)
                region_positions.append(y)
                region = image_bin[y:y+h+1,x:x+w+1]
                regions_dict[x] = [img_fun.resize_region(region), (y, x, w, h)]
                cv2.rectangle(image_orig, (x, y), (x+w, y), (0, 255, 0), 2)

        sorted_regions_dict = collections.OrderedDict(sorted(regions_dict.items()))
        sorted_regions = np.array(sorted_regions_dict.values())

        self.h_lines = regions

        return image_orig, sorted_regions[:, 0], region_positions