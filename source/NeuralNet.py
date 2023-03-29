import numpy as np
import random

from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Dropout, Activation, Flatten, Input, BatchNormalization
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist

#from keras.applications.vgg16 import preprocess_input
#from keras.applications.vgg16 import VGG16

#from keras.applications.vgg19 import preprocess_input
#from keras.applications.vgg19 import VGG19

from keras.applications.resnet_v2 import ResNet152V2
from keras.applications.resnet_v2 import preprocess_input

from DataSet import *
from Image import *

import pickle
from zipfile import ZipFile

import shutil


class NeuralNet(Sequential):
    def __init__(self, inputShape, labels, custom=False, fileName=None):
        """
        Initialise le réseau
        :Param custom: bool à True si la configuration des couches et la compilation du domaine est par défaut
                    si False: il faut ajouter les couches manuellement et compiler le modèle manuellement
        :Param inputShape: dimension des entrées du réseau de neurones
        :Param labels: liste des labels
        :Param fileName: utilisé pour recharger le réseau de neurone
        """
        super().__init__()

        if fileName != None: #reconstruction à vide à partir d'un fichier de sauvegarde
            with open(fileName, "rb") as file:
                self.labels, self.inputShape = pickle.load(file)
            nClasse = len(self.labels)
        else:
            self.labels = labels
            nClasse = len(self.labels) # nombre de classe à distinguer
            self.inputShape = inputShape #dimension de l'input du réseau

        self.labels = [lab.strip() for lab in self.labels]
        if not custom:
            #self.add(VGG19(input_shape = self.inputShape,include_top = False, weights = 'imagenet'))
            self.add(ResNet152V2(input_shape = self.inputShape,include_top = False, weights = 'imagenet'))

            for layer in self.layers:# pas besoin d'entrainer les couches du modèle pré-
                layer.trainable = False

            #self.add(BatchNormalization())
            self.add(Flatten())
            self.add(Dense(nClasse, activation='softmax'))

            self.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])# compile le modèle, pas très intéressant

    def fit(self, X_train, Y_train, batchSize=32, nEpoch=10, verbose=0, useMultiprocessing=False):
        """
        Entraîne le modèle sur les nTrain premières images du modèle
        :Param X_train: matrices des images à entrainer
        :Param Y_train: matrices des outputs espérés
        :Param batchSize: nombre d'images par batch
        :Param nEpoch: nombre d'époque
        :Param verbose: int:    0: affiche aucune information sur le résultat
                                1: affiche en détail la progression de l'entrainement
                                2: affiche un résumé de l'entrainement après chaque époque
        :Param useMultiprocessing: True si multi processing
        :return: None
        """
        X_train = preprocess_input(X_train)
        #X_train = X_train.astype("float32")/255

        super().fit(X_train, Y_train, batch_size=batchSize, epochs=nEpoch, verbose=verbose, use_multiprocessing=useMultiprocessing)

    def evaluate(self, X_test, Y_test, verbose=0, useMultiprocessing=False):
        """
        Evalue le modèle grâce qu nTest dernières images du modèles
        :Param X_test: matrices des images à entrainer
        :Param Y_test: matrices des outputs espérés
        :Param verbose: int:    0: affiche aucune information sur le résultat
                                1: affiche en détail la progression de l'entrainement
        :Param useMultiprocessing: True si multi processing
        :return: un tuple contenant les ratios: (loss, accuarcy)
        """
        X_test = preprocess_input(X_test)
        #X_test = X_test.astype("float32")/255

        return super().evaluate(X_test, Y_test, verbose=verbose, use_multiprocessing=useMultiprocessing)

    def predict(self, img, normalized=False, batch_size=None, verbose=0, steps=None, callbacks=None, max_queue_size=10, workers=1, use_multiprocessing=False):
        """
        Prédit la classe de l'image x donnée en input
        :Param img: Objet de type Image
        :Param normalized: Bool:    True: les valeurs de x sont normalisées entre 0 et 1
                                    False: les valeurs de x ne sont pas normalisées (donc entre 0 et 255)
        :Autres params: paramètres disponibles avec la méthode model.predict
        :return: liste triée en fonction des probabilités de tuples (label, prob)
        """
        img.rescale(self.inputShape[0], self.inputShape[1])
        img.crop(self.inputShape[0], self.inputShape[1])

        x = img.repr()[None,:]
        x = preprocess_input(x)
        prediction = list(super().predict(x, batch_size=batch_size, verbose=verbose, steps=steps, callbacks=callbacks, max_queue_size=max_queue_size,workers=workers, use_multiprocessing=use_multiprocessing)[0])

        predictions = [(lab,prob) for lab,prob in zip(self.labels, prediction)]
        predictions.sort(key=lambda tup: tup[1], reverse=True)#tri en fonction des probabilités

        return predictions

    def save(self, fileName, erase=False, saveOnlyTrainable=True):
        """
        sauvegarde un réseau de neurone dans un fichier
        :Param net: NeuralNet à sauvegarder
        :Param fileName: nom du fichier où le réseau est sauvegardé
        :Param erase: si True écrase le fichier fileName s'il existe (attention donc)
        :Param saveOnlyTrainable: True: sauvegarde uniquement les couches entrainables
        :return: None
        """
        assert erase or not os.path.exists(fileName), "{} existe".format(fileName)
        tmpDir = "./tmp/"
        if not os.path.exists(tmpDir):
            os.mkdir(tmpDir)

        with open(tmpDir+"info.pickle", "wb") as file:
            pickle.dump((self.labels, self.inputShape), file)

        i = 0
        weights_file = []
        for layer in self.layers:
            if layer.trainable or not saveOnlyTrainable: #on suppose que les couches non entrainables sont celle d'un réseau pré entrainé
                path = tmpDir+"layer{}.pickle".format(str(i))
                weights_file.append(path)
                with open(path, "wb") as file:
                    pickle.dump(layer.get_weights(), file)
            i+=1

        #net.save_weights(tmpDir+"weights.h5")
        with ZipFile(fileName,'w') as zip:
            zip.write(tmpDir+"info.pickle")
            #zip.write(tmpDir+"weights.h5")
            for path in weights_file:
                zip.write(path)

        shutil.rmtree(tmpDir, ignore_errors=True)




def doubleShuffle(l1, l2):
    """
    fonction qui mélange 2 listes de même taille de la même manièrevie
    les mêmes permutations sont faites pour les 2 listes
    """
    randomN = random.random()
    f = lambda: randomN
    random.shuffle(l1, f)
    random.shuffle(l2, f)

def loadNerualNetOld(fileName):
    """
    charge un réseau de neurone à partir d'un fichier (ANCIENNE méthode)
    :Param fileName: fichier de sauvegarde
    :return NeuralNet:
    """
    assert os.path.exists(fileName), "{} n'existe pas".format(fileName)
    tmpDir = "./tmp"
    infoFile = "./tmp/info.pickle"
    weightFile = "./tmp/weights.h5"
    with ZipFile(fileName, 'r') as zip:
        zip.extractall()
    loaded_model = NeuralNet(None, None, fileName=infoFile)
    # load weights
    loaded_model.load_weights(weightFile)

    shutil.rmtree(tmpDir, ignore_errors=True)
    return loaded_model

def loadNerualNet(fileName):
    """
    charge un réseau de neurone à partir d'un fichier
    :Param fileName: fichier de sauvegarde
    :return NeuralNet:
    """
    assert os.path.exists(fileName), "{} n'existe pas".format(fileName)
    tmpDir = "./tmp"
    infoFile = "./tmp/info.pickle"
    weightFile = "./tmp/weights.h5"
    with ZipFile(fileName, 'r') as zip:
        zip.extractall()
    loaded_model = NeuralNet(None, None, fileName=infoFile)
    # load weights
    # loaded_model.load_weights(weightFile)
    i=0
    for layer in loaded_model.layers:
        path = tmpDir+"/layer"+str(i)+".pickle"
        if os.path.exists(path):
            with open(path, "rb") as file:
                layer_weights = pickle.load(file)
                layer.set_weights(layer_weights)
        i+=1

    shutil.rmtree(tmpDir, ignore_errors=True)
    return loaded_model



def extractDataSet(dataSet, nTrain, nTest):
    """
    instancie Récupère les données X,Y,label du dataset
    :Param nTrain: nombre d'image destinée à l'entrainement
    :Param nTest: nombre d'image destinée aux tests
    :return: (X_train, Y_train, X_test, Y_test, labels)
    """

    dataSet.shuffle()
    X = dataSet.getX()
    y, labels = dataSet.getY()
    #doubleShuffle(X, y) #mélange X et y tel que les 2 listes restent cohérantes entre elles

    X = np.array(X)# erreur si toutes les images n'ont pas les mêmes dimensions
    Y = np_utils.to_categorical(np.array(y), len(labels))

    if nTrain>len(y):
        nTrain = len(y)
    if nTest>len(y):
        nTest = len(y)

    if nTrain + nTest > len(y):
        print("Attention: certaines images de test sont dans le jeu d'entrainement  ")

    X_train, Y_train = X[:nTrain], Y[:nTrain]
    X_test, Y_test = X[len(y)-nTest:], Y[len(y)-nTest:]

    return (X_train, Y_train, X_test, Y_test, labels)


if __name__ == "__main__":
    path = "/home/simon/Téléchargements/data_smallOctavius/"
    #path = "/home/simon/Téléchargements/dataSet/"
    ds = DataSet(path+"train", "jpeg")

    X_train, Y_train, X_test, Y_test, labels = extractDataSet(ds, 99999, 0) # charge toutes les images du dossier (image d'entrainement)


    ds = DataSet(path+"test", "jpeg")
    a, b, X_test, Y_test, labels = extractDataSet(ds, 0, 999999) # charge les images de contrôle

    ds = None
    #octavius = NeuralNet((224,224,3), labels) #création d'un nouveau réseau
    octavius = loadNerualNet("./ressource/savedNetwork/smallOctavius_82") #charge un réseau existant

    try:
        print("Begin evaluation")
        octavius.fit(X_train, Y_train, verbose=1, nEpoch=5, batchSize=2500 )
        octavius.evaluate(X_test, Y_test, verbose=1)
    except KeyboardInterrupt:
        print("Abbord")
        octavius.save("./ressource/savedNetwork/smallOctavius_save", True) # sauvegarde le réseau

    octavius.save("./ressource/savedNetwork/smallOctavius", True)
