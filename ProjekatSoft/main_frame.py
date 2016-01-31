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

        self.buttonPlay = Button(self, text="Play")
        self.buttonPlay["command"] = self.play_sheet
        self.buttonPlay.grid()

    def train_ann(self):
        image = cv2.imread("images/train_rests_beams.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        ret, image_bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)


        image_bin = imgFunctions.invert(image_bin);

        groups = self.get_groups(image)
        image_orig,selected_regions, positions = imgFunctions.select_roi(image.copy(), image_bin,groups)

        positions = np.array(positions).reshape(len(positions), 1)
        print positions

        cv2.imshow('binary', image_orig)


        self.alphabet = ['g-key', 'time-sig-4/4', '1', '2', '4', '8','8','4','2','rest-1','rest-2','rest-4','rest-8','beam-8']
        inputs = ann_fun.prepare_for_ann(selected_regions)
        outputs = ann_fun.convert_output(self.alphabet)

        notes = np_fun.get_notes(image)

        self.ann = ann_fun.create_ann()
        self.ann = ann_fun.train_ann(self.ann, inputs, outputs)

        results = self.ann.predict(np.array(inputs, np.float32))
        results = ann_fun.display_result(results, self.alphabet)

        print results

        print 'done'

    def predict_ann(self):
        filename = tkFileDialog.askopenfilename()
        print filename
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        ret, image_bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)


        image_bin = imgFunctions.invert(image_bin);



        groups = self.get_groups(image)

        print "groups"
        print len(groups)

        image_orig,selected_regions, positions = imgFunctions.select_roi(image.copy(), image_bin, groups)

        positions = np.array(positions).reshape(len(positions), 1)
        print positions

        cv2.imshow('binary', image_orig)



        self.inputs = ann_fun.prepare_for_ann(selected_regions)
        self.outputs = ann_fun.convert_output(self.alphabet)

        self.notes = np_fun.get_notes(image)

        # for i in range(len(self.notes)):
        #     self.notes[i].print_note()

        results = self.ann.predict(np.array(self.inputs, np.float32))
        results = ann_fun.display_result(results, self.alphabet)
        print results
        results = self.replace_beams(results)
        print results




        #print results

    def play_sheet(self):
        play.play(self.ann, self.notes, self.inputs, self.outputs, self.alphabet)


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