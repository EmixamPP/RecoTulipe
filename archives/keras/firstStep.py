# 1. Import libraries and modules

from keras.datasets import mnist
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
from keras.utils import np_utils

# 2. Load pre-shuffled MNIST data into train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# X_train -> matrice de taille (60000, 28, 28) est 60000 images d'entrainements
# y_train -> liste de taille 60000 qui correspond au labels des images d'entrainement
# X_test -> matrice de taille (10000, 28, 28) est 10000 images de tests
# y_train -> liste de taille 60000 qui correspond au labels des images de test


# 3. Preprocess input data
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1) #rajoute une dimension à X_train (je ne suis pas sur mais je pense que c'est pour les réseaux convolutifs)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255 #valeur enter 0 et 1
X_test /= 255



# 6. Preprocess class labels
Y_train = np_utils.to_categorical(y_train, 10) # transforme un entier liste avec que des 0 sauf à l'emplacement correspondant à l'entiers
Y_test = np_utils.to_categorical(y_test, 10)

# 7. Define model architecture
model = Sequential()

model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(28,28,1))) #couche convolutive
# 32 -> nombre de filtre
# (3,3) -> tailel de la fenêtre du réseau
# 'relu' -> fonction d'activation des neurones
model.add(Convolution2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
#diminue la taille de la couche préceédente en prenant le neurone avec la valeur max dans une fenêtre de (2,2)
model.add(Dropout(0.25))
#met aléatoirement avec une probabilité de 1/4 des neurones de la couche à 0 (c'est bien pour que le modèles soit plus efficace sur des nouvelles images si j'ai bien compris)

model.add(Flatten())#applatit la couche. Avant, c'était une matrice à plusieurs dimension. Après applatit en un vecteur colonne pour les couches suivantes
model.add(Dense(16, activation='relu'))
#couche traditionnelle avec 16 neurones et relu comme fonction d'activation
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))


"""
model.add(Flatten())
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(10, activation='sigmoid'))
"""

# 8. Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])# compile le modèle, pas très intéressant

# 9. Fit model on training data
model.fit(X_train, Y_train, batch_size=32, epochs=10, verbose=1) # entraine le modèle avec des batch de 32 images et sur 10 époques (répète l'entrainement 10 fois)
