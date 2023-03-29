# 1. Import libraries and modules
import numpy as np
from keras.applications.resnet import ResNet50 as pretrainedModel
from keras.applications.resnet import preprocess_input
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
from keras.utils import np_utils

# 2. Load pre-shuffled MNIST data into train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

n_train = 100  # nombre d'images d'entraînements souhaitées
n_test = 1000  # nombre d'images de tests souhaitées

# réduit la taille des listes
X_train = X_train[:n_train]
y_train = y_train[:n_train]

X_test = X_test[:n_test]
y_test = y_test[:n_test]

# traitement pour que les images soient acceptées par le réseau
n_scale = 3
X_train = np.kron(X_train, np.ones((1,n_scale,n_scale)))#met à l'échelle les images par n_scale
X_train = np.repeat(X_train[:,:,:, np.newaxis], 3, axis=3)#met les images en RGb

X_test = np.kron(X_test, np.ones((1,n_scale,n_scale)))#upscale les images par 2
X_test = np.repeat(X_test[:,:,:, np.newaxis], 3, axis=3)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255 #valeur enter 0 et 1
X_test /= 255


# 6. Preprocess class labels
Y_train = np_utils.to_categorical(y_train, 10) # transforme un entier liste avec que des 0 sauf à l'emplacement correspondant à l'entiers
Y_test = np_utils.to_categorical(y_test, 10)

X_train = preprocess_input(X_train)
X_test = preprocess_input(X_test)


model = Sequential()
#utilsie le modèle pré-entraîné en modifiant la couche d'input et en retirant l'output
model.add(pretrainedModel(input_shape = (28*n_scale, 28*n_scale, 3), include_top = False, weights = 'imagenet'))

for layer in model.layers:# pas besoin d'entrainer les couches du modèle pré-entrainé
	layer.trainable = False

#applatit la couche
model.add(Flatten())
model.add(Dropout(0.1)) # pour que le modèle soit plus robuste sur les données inconnues
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))


model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])# compile le modèle, pas très intéressant
model.fit(X_train[:100], Y_train[:100], batch_size=32, epochs=10, verbose=1) # entraine le modèle avec des batch de 32 images et sur 10 époques (répète l'entrainement 10 fois)

score=model.evaluate(X_test, Y_test, verbose=1)[1]# teste de l'efficacité du modèle
print("Accuracy:", score)
