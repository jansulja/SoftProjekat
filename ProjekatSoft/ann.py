from keras.models import Sequential
from keras.layers.core import Dense,Activation
from keras.optimizers import SGD
import numpy as np
import cv2
import ann_functions as ann_fun

class Ann:

    def __init__(self,x_train,y_train):
        self.ann = ann_fun.create_ann()
        self.x_train = x_train
        self.y_train = y_train

    def train(self):
        self.ann = ann_fun.train_ann(self.ann,self.x_train,self.y_train)

