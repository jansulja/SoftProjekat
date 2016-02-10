from __future__ import division
from Tkinter import *
import tkFileDialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
import collections

from matplotlib.text import _AnnotationBase
from sklearn import datasets
from sklearn.cluster import KMeans
import ann_functions as ann_fun
import imageProcessingFunctions as imgFunctions
import note_positions_fun as np_fun
import soundGenerator as sgen
import play_sheet as play
import note_positions_fun as nt_fun
import imageProcessingFunctions as img_fun
import ttk
from os import listdir
from os.path import isfile, join
import accidentals_elimination_fun as acc_fun
import player as pl

class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_components()

    def create_components(self):



        self.buttonTrain = Button(self, text="Train")
        self.buttonTrain["command"] = self.train_ann
        self.buttonTrain.grid()

        self.buttonPredict = Button(self, text="Predict")
        self.buttonPredict["command"] = self.predict_ann
        self.buttonPredict.grid()

        self.current_sf = 'JR_organ.sf2'

        self.box_value = StringVar()
        self.box = ttk.Combobox(self, textvariable=self.box_value)
        self.box['values'] = tuple(self.get_available_sound_fonts())
        self.box.current(0)
        self.box.bind("<<ComboboxSelected>>", self.new_selection)
        self.box.grid()



        self.buttonPlay = Button(self, text="Play")
        self.buttonPlay["command"] = self.play_sheet
        self.buttonPlay.grid()

    def get_available_sound_fonts(self):
        onlyfiles = [f for f in listdir('sound_fonts/') if isfile(join('sound_fonts/', f))]
        return  onlyfiles

    def new_selection(self,event):
        self.current_sf = self.box_value.get()

    def train_ann(self):
        image = cv2.imread("images/train_rets.png")

        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # ret, image_bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        # image_bin = imgFunctions.invert(image_bin);

        image_bin = self.prepare_image(image)
        groups = self.get_groups(image)
        image_orig,selected_regions, positions,reg_details = imgFunctions.select_roi(image.copy(), image_bin,groups)

        positions = np.array(positions).reshape(len(positions), 1)

        cv2.imshow('training', image_orig)

        self.alphabet = ['g-key', 'time-sig-4/4', '1', '2', '4', '8','8','4','2', 'rest-1', 'rest-2','rest-4', 'rest-8']

        inputs = ann_fun.prepare_for_ann(selected_regions)
        outputs = ann_fun.convert_output(self.alphabet)

        # notes = np_fun.get_notes(image)

        self.ann = ann_fun.create_ann(len(self.alphabet))
        self.ann = ann_fun.train_ann(self.ann, inputs, outputs)

        results = self.ann.predict(np.array(inputs, np.float32))
        results = ann_fun.display_result(results, self.alphabet)


        print 'done'

    def prepare_image(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, image_bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        image_bin = imgFunctions.invert(image_bin);

        cv2.imshow('bin',image_bin)

        return image_bin


    def predict_ann(self):
        filename = tkFileDialog.askopenfilename()
        image = cv2.imread(filename)
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # ret, image_bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        # image_bin = imgFunctions.invert(image_bin);

        image_bin = self.prepare_image(image)
        groups = self.get_groups(image)


        image_orig,selected_regions, positions,reg_details = imgFunctions.select_roi(image.copy(), image_bin, groups)



        self.inputs = ann_fun.prepare_for_ann(selected_regions)
        self.outputs = ann_fun.convert_output(self.alphabet)


        self.sheet = np_fun.get_notes(image)
        #
        results = self.ann.predict(np.array(self.inputs, np.float32))
        results = ann_fun.display_result(results, self.alphabet)
        print results

        #results = ['g-key', 'time-sig-4/4', '4', '4', '2', '4', '4', '2', '4', '4', '4', '4', '1', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '2', '2']

        self.chords = self.sheet.set_chords_duration(results[2:])

        #
        # print "length"
        # print len(reg_details)
        # print len(results)
        # cv2.imshow('selected regions', image_orig)
        #
        # results = self.replace_beams(results)
        # print results
        #
        # # img_no_acc = acc_fun.eliminate(image.copy(),results,reg_details)
        # # cv2.imshow('no acc', img_no_acc)
        #
        # positions = np.array(positions).reshape(len(positions), 1)
        #
        # cv2.imshow('binary', image_orig)

    def play_sheet(self):
        #play.play(self.ann, self.notes, self.inputs, self.outputs, self.alphabet, self.current_sf)


        player = pl.Player(self.sheet)
        player.play_sheet(self.chords,self.current_sf)

    def get_groups(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        ret, image_bin = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

        image_bin=img_fun.invert(image_bin)

        horizontalsize = 200;
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1));

        image_bin = cv2.erode(image_bin, horizontalStructure, iterations=1)
        image_bin = cv2.dilate(image_bin,horizontalStructure, iterations=1)

        image_orig, selected_regions, lines = nt_fun.select_horizontal_lines(image.copy(), image_bin)

        lines,groups = nt_fun.add_additional_lines(lines)

        return groups

    def replace_beams(self,results):
        new_res = []
        for i in range(len(results)):
            if results[i] == 'beam-8':
                new_res.append('8')
                new_res.append('8')
            else:
                new_res.append(results[i])

        return new_res