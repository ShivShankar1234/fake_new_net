import numpy as np
import matplotlib.pyplot as plt
import scikitplot as skplt

from tensorflow import keras
from keras import backend as K
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, Input, RepeatVector



"""Plots confustion matrix."""
def plot_cmat(y_test, y_pred):
    skplt.plot_confusion_matrix(y_test, y_pred)
    plt.show()

x_train, x_test, y_test, y_train = getEmbeddings("datasets/train.csv")



""" Basic Neural Network"""
def baseline_model():
    model = Sequential()
    model.add(Dense(256, input_dim=300, activation='relu', kernel_initializer='normal'))
    model.add(Dropout(0.3))
    model.add(Dense(256, activation='relu', kernel_initializer='normal'))
    model.add(Dropout(0.5))
    model.add(Dense(80, activation='relu', kernel_initializer='normal'))
    model.add(Dense(2, activation='softmax', kernel_initializer='normal'))

    sgd = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model

