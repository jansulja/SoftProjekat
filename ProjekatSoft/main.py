from __future__ import division
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


image = cv2.imread("images/sheet4.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


ret, image_bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)


image_bin = imgFunctions.invert(image_bin);
image_orig,selected_regions, positions = imgFunctions.select_roi(image.copy(), image_bin)

positions = np.array(positions).reshape(len(positions), 1)
print positions

'''
k_means = KMeans(n_clusters=8, max_iter=5000, init='random', tol=0.00001, n_init=10)
k_means.fit(positions)
print k_means.cluster_centers_
'''


cv2.imshow('binary', image_orig)
cv2.waitKey(0)

alphabet = ['g-key', 'time-sig-4/4', '1', '2', '4', '8']
inputs = ann_fun.prepare_for_ann(selected_regions)
outputs = ann_fun.convert_output(alphabet)

notes = np_fun.get_notes(image)
'''
for i in range(len(notes)):
    notes[i].print_note()
    sgen.playNote(notes[i].frequency, notes[i].duration)
'''
#ann = ann_fun.create_ann()
#ann = ann_fun.train_ann(ann, inputs, outputs)

print 'done'

#results = ann.predict(np.array(inputs, np.float32))

#results = ann_fun.display_result(results,alphabet)

#for i in range(2,len(results)):
#    notes[i].set_duration(1/results[i])


