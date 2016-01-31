from keras.models import Sequential
from keras.layers.core import Dense,Activation
from keras.optimizers import SGD
import numpy as np
import cv2


def create_ann():

    ann = Sequential()
    ann.add(Dense(128, input_dim=784, activation='sigmoid'))
    ann.add(Dense(14, activation='sigmoid'))
    return ann


def train_ann(ann, x_train, y_train):
    x_train = np.array(x_train, np.float32)
    y_train = np.array(y_train, np.float32)
    sgd = SGD(lr=0.01, momentum=0.9)
    ann.compile(loss='mean_squared_error', optimizer=sgd)
    ann.fit(x_train, y_train, nb_epoch=500, batch_size=1, verbose=0, shuffle=False, show_accuracy=False)
    return ann


def resize_region(region):
    resized = cv2.resize(region,(28,28), interpolation=cv2.INTER_NEAREST)
    return resized


def scale_to_range(image):
    return image / 255


def matrix_to_vector(image):
    return image.flatten()


def prepare_for_ann(regions):
    ready_for_ann = []
    for region in regions:
        ready_for_ann.append(matrix_to_vector(scale_to_range(region)))
    return ready_for_ann


def convert_output(outputs):
    return np.eye(len(outputs))


def winner(output):
    return max(enumerate(output), key=lambda x: x[1])[0]


def display_result(outputs, alphabet):

    result = []
    for output in outputs:
        result.append(alphabet[winner(output)])
    return result
