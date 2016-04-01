from __future__ import division
from Tkinter import *
import tkFileDialog
import cv2
import numpy as np
import ann_functions as ann_fun
import imageProcessingFunctions as imgFunctions
import note_positions_fun as nt_fun
import imageProcessingFunctions as img_fun
import ttk
from os import listdir
from os.path import isfile, join
import player as pl
import notebook as ntbook
import threading
import acc_handler as acch
import serialize as se
import pickle
import note_positions_fun as np_fun
import tkMessageBox

class Application(Frame):

    from_notebook = 0

    def __init__(self, master):
        Frame.__init__(self, master)

        self.grid()
        self.create_components()
        self.alphabet = ['g-key', 'time-sig-4/4', '1', '2', '4', '8','8','4','2', 'rest-1', 'rest-2','rest-4', 'rest-8', 'beam-8','beam-8', 'beam-8','beam-8', 'beam-8','beam-8']



    def create_components(self):

        toolbar = Frame(self.master, bd=1, relief=RAISED)
        # buttonTest = Button(toolbar, text= "EXIT",relief=FLAT, command=self.quit)
        # buttonTest.pack(side=LEFT, padx=2, pady=2)
        # toolbar.pack(side=RIGHT, fill=X)

        self.buttonTrain = Button(toolbar, text="Train")
        self.buttonTrain["command"] = self.train_ann
        self.buttonTrain.pack(side=LEFT, padx=2, pady=2)
        # self.buttonTrain.grid()

        self.label = ttk.Label(toolbar,text="")
        self.label.pack(side=LEFT, padx=2, pady=2)


        self.progressbar = ttk.Progressbar(toolbar,orient=HORIZONTAL, length=200, mode='determinate')
        # self.progressbar.pack(side=LEFT, padx=2, pady=2)


        self.buttonPredict = Button(toolbar, text="Load sheet")
        self.buttonPredict["command"] = self.predict_ann
        self.buttonPredict.pack(side=LEFT, padx=30, pady=2)




        self.buttonPredict = Button(toolbar, text="From sheet notebook")
        self.buttonPredict["command"] = self.take_picture
        #self.buttonPredict.pack(side=LEFT, padx=2, pady=2)

        self.current_sf = '1115-Chitarra Acustica CORT.sf2'

        self.box_value = StringVar()
        self.box = ttk.Combobox(toolbar, textvariable=self.box_value)
        self.box['values'] = tuple(self.get_available_sound_fonts())
        self.box.current(0)
        self.box.bind("<<ComboboxSelected>>", self.new_selection)
        self.box.pack(side=LEFT, padx=30, pady=2)




        self.buttonPlay = Button(toolbar, text="Play sheet")
        self.buttonPlay["command"] = self.play_sheet
        self.buttonPlay.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=BOTH)




    def get_available_sound_fonts(self):
        onlyfiles = [f for f in listdir('sound_fonts/') if isfile(join('sound_fonts/', f))]
        return  onlyfiles

    def new_selection(self,event):
        self.current_sf = self.box_value.get()

    def train(self):
        self.label["text"] = "Training in progress.."
        self.label["foreground"] = 'red'

        self.progressbar.start(140)

        self.t = threading.Thread()
        self.t.__init__(target = self.train_ann, args = ())
        self.t.start()

        # self.progressbar.stop()

    def train_ann(self):



        image = cv2.imread("images/train.png")
        image_bin = self.prepare_image(image)
        groups = self.get_groups(image)
        image_orig,selected_regions, positions,reg_details = imgFunctions.select_roi(image.copy(), image_bin,groups)

        # cv2.imshow('bin',image_bin)
        # cv2.waitKey(0)
        #
        # cv2.imshow('bin',image_orig)
        # cv2.waitKey(0)


        inputs = ann_fun.prepare_for_ann(selected_regions)
        outputs = ann_fun.convert_output(self.alphabet)

        # notes = np_fun.get_notes(image)

        self.ann = ann_fun.create_ann(len(self.alphabet))
        self.ann = ann_fun.train_ann(self.ann, inputs, outputs)


        saver = se.Serialize('trained_ann.pkl',self.ann)
        saver.save()

        results = self.ann.predict(np.array(inputs, np.float32))

        results = ann_fun.display_result(results, self.alphabet)


        self.progressbar.stop()
        self.label["text"] = "Done"
        self.label["foreground"] = '#437C17'




        tkMessageBox.showinfo("Info", "Done!")

    def prepare_image(self,image):

        acc_handler = acch.Acc_handler(image)
        image_bin = acc_handler.remove_accs()



        return image_bin






    def predict_ann(self):
        filename = tkFileDialog.askopenfilename(initialdir='images/')
        image = cv2.imread(filename)
        if image is None:
            return

        image_bin = self.prepare_image(image)
        groups = self.get_groups(image)

        image_orig,selected_regions, positions,reg_details = imgFunctions.select_roi(image.copy(), image_bin, groups)

        self.inputs = ann_fun.prepare_for_ann(selected_regions)
        self.outputs = ann_fun.convert_output(self.alphabet)


        self.sheet = np_fun.get_notes(image)


        with open('saved_ann/trained_ann.pkl', 'rb') as input:
            self.ann = pickle.load(input)

        results = self.ann.predict(np.array(self.inputs, np.float32))
        print 'results = ',results
        results = ann_fun.display_result(results, self.alphabet)
        results = self.replace_beams(results)
        print results

        self.chords = self.sheet.set_chords_duration(results[2:])

        tkMessageBox.showinfo("Done", "Sheet loaded. Click on Play Sheet button.")

        img_fun.show_image('Sheet',image)



    def take_picture(self):

        # camera = cam.Camera()
        # image = camera.show_webcam(False)
        image = cv2.imread("images/camera/b.jpg")

        Application.from_notebook = 1

        notebook = ntbook.Notebook(image)

        Application.from_notebook = 0





    def play_sheet(self):
        #play.play(self.ann, self.notes, self.inputs, self.outputs, self.alphabet, self.current_sf)
        if hasattr(self,'sheet'):

            player = pl.Player(self.sheet)
            player.play_sheet(self.chords,self.current_sf)
        else:
            tkMessageBox.showerror("Error","Sheet not loaded. Click on Load sheet button first.")



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

