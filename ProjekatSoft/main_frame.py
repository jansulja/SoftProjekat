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
        image = cv2.imread("images/train3.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        ret, image_bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)


        image_bin = imgFunctions.invert(image_bin);
        image_orig,selected_regions, positions = imgFunctions.select_roi(image.copy(), image_bin)

        positions = np.array(positions).reshape(len(positions), 1)
        print positions

        cv2.imshow('binary', image_orig)


        self.alphabet = ['g-key', 'time-sig-4/4', '1', '2', '4', '8','8','4','2']
        inputs = ann_fun.prepare_for_ann(selected_regions)
        outputs = ann_fun.convert_output(self.alphabet)

        notes = np_fun.get_notes(image)

        self.ann = ann_fun.create_ann()
        self.ann = ann_fun.train_ann(self.ann, inputs, outputs)

        print 'done'

    def predict_ann(self):
        filename = tkFileDialog.askopenfilename()
        print filename
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        ret, image_bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)


        image_bin = imgFunctions.invert(image_bin);
        image_orig,selected_regions, positions = imgFunctions.select_roi(image.copy(), image_bin)

        positions = np.array(positions).reshape(len(positions), 1)
        print positions

        cv2.imshow('binary', image_orig)



        self.inputs = ann_fun.prepare_for_ann(selected_regions)
        self.outputs = ann_fun.convert_output(self.alphabet)

        self.notes = np_fun.get_notes(image)

        #results = self.ann.predict(np.array(self.inputs, np.float32))

        #results = ann_fun.display_result(results, self.alphabet)

        # print results

    def play_sheet(self):
        play.play(self.ann, self.notes, self.inputs, self.outputs, self.alphabet)

