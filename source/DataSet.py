import copy
import errno
import glob
import multiprocessing
import os
import random

import imageio.core.util

from Image import Image


def ignore_warnings(*args, **kwargs):
    pass


imageio.core.util._precision_warn = ignore_warnings


class DataSet:
    def __init__(self, pathToDataSet, extension, shuffle=True, process=-1):
        """
        :param pathToDataSet: emplacement du data set qui doit être un repertoire non compressé et il doit comprendre
        des sous repertoires qui sont les classes des images. Le nom de ces sous dossiers serviront de label aux images
        qu'ils contiennent.
        :param extension: format des images du data set ex : png, jpg, jpeg ...
        :param shuffle: si True mélange l'ordre des images du dataset
        :param process: nombre de process à utiliser pour effectuer les opérations: au minimum 1 et mettre la valeur -1
        pour utiliser tout les coeurs (physique et logique) du CPU
        """
        self.extension = "." + extension
        self.images = []  # liste des objets Images
        self.labels = []  # liste des labels possible

        self.nbr_process = process if process > 0 else multiprocessing.cpu_count()
        self.running_process = []
        self.X_range_process = []
        # indice de séparation du tableau en process, chaque process aura un tuple (start, end) qui correspont au indice
        # de la matrice images de start jusqu'à end non compris

        c = -1
        olabel = ""
        dirPath = glob.glob(pathToDataSet + "/" + "**/*." + extension, recursive=True)
        if not len(dirPath):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), pathToDataSet)

        for imgPath in dirPath:
            # le label est le nom du dernier repertoire composant le chemin
            i = imgPath.rfind("/")
            j = imgPath.rfind("/", 0, i)
            nlabel = imgPath[j + 1: i]  # label de l'image actuelle

            if nlabel != olabel:  # quand on changera de répertoire le label changera
                self.labels.append(nlabel)  # il y a donc une nouvelle classe de data
                c += 1  # position du label dans la liste

            self.images.append(Image(imgPath, c))

            olabel = nlabel  # label de la précédente image

        i = 0  # calcul de self.X_range_process
        while i < self.nbr_process - 1:
            self.X_range_process.append(
                (i * len(self.images) // self.nbr_process, (i + 1) * len(self.images) // self.nbr_process))
            i += 1
        self.X_range_process.append((i * len(self.images) // self.nbr_process, len(self.images)))

        if shuffle:
            self.shuffle()

    def rescale(self, height, width):
        """
        Redimentionne l'image en gardant le radio. Exemple sur des images en 30x50 on les veut en 20x20 alors
        les images seront en 12x20.
        :param height: hauteur voulue
        :param width: largeur voulue
        :return:
        """
        self.__run_process__(__process_rescale__, height, width)

    def resize(self, height, width):
        """
        Redimentionne les images en ignorant le radio
        :param height: hauteur voulue
        :param width: largeur voulue
        :return:
        """
        self.__run_process__(__process_resize__, height, width)

    def crop(self, height, width):
        """
        Coupe les images à partir du centre de celle-ci
        :param height: hauteur voulue
        :param width: largeur voulue
        :return:
        """
        self.__run_process__(__process_crop__, height, width)

    def save(self, pathToSave):
        """
        Enregistre les images à un emplacement donné
        :param pathToSave: emplacement à enregistrer le data set
        :return: -1 si l'emplacement existe déjà, 0 si succes
        """
        try:
            os.mkdir(pathToSave)
        except FileExistsError:
            print(pathToSave, "est déjà un repertoire existant, veuillez indiquez un repertoire à créer")
            return -1

        for label in self.labels:
            os.mkdir(pathToSave + "/" + label)

        c = 0  # nouveau nom de l'image
        for img in self.images:
            img.save(pathToSave + "/" + self.labels[img.getLabel()] + "/" + str(c) + self.extension)
            c += 1
        return 0

    def unsharpGaussianFilter(self, sigma=5, factor=2):
        """
        Supprime le bruit/flou des images
        https://scikit-image.org/docs/dev/auto_examples/filters/plot_unsharp_mask.html
        enhanced image = original + factor * (original - blurred)
        :param sigma: écart type pour la fonction de Gauss. Plus il est grand moins il y aura de flou.
        :param factor: facteur d'accentuation
        :return:
        """
        self.__run_process__(__process_unsharpGaussianFilter__, sigma, factor)

    def getX(self, quantity=-1, gray=False):
        """
        :param quantity: nombre d'image a retourner (le data set sera shuffle). -1 pour tout selectionner.
        Si le nombre d'images demandé dépasse la taille du data set alors quantity sera considéré comme valant -1.
        :param gray: si vrai les images seront données en nuance de gris (2D)
        :return: une matrice avec sur chaque ligne une matrice qui est la représentation de l'image
        """
        if 0 < quantity <= len(self.images):
            self.shuffle()
            return [copy.deepcopy(img.repr(gray)) for img in self.images[0:quantity]]
        else:
            return [copy.deepcopy(img.repr(gray)) for img in self.images]

    def getY(self):
        """
        :return: un tuple (une matrice avec sur chaque ligne i un entier j correspondant à l'image de la matrice X[i],
        une liste [label1, label2, ...] où chaque entier j à son label correspondant à la position j de cette liste)
        """
        return [img.getLabel() for img in self.images], self.labels

    def setX(self, X):
        """
        Change la matrice de représentation des imgages data set par la matrice X, cette méthode est prévue pour
        mettre à jour le data set après avoir fait des prétraitements. A utiliser de manière consciencieuse.
        :param X: matrice de représentation des images
        :return: -1 si la taille de la matrice X n'est pas la même que celle déjà présente dans le data set sinon 0
        """
        if len(X) != len(self.images):
            print("setX : il n'y a pas le même nombre d'images dans la nouvelle matrice X")
            return -1

        for i in range(len(X)):
            self.images[i] = Image(X[i], self.images[i].getLabel())
        return 0

    def shuffle(self):
        """
        Mélange l'ordre des images du dataset
        :return:
        """
        random.shuffle(self.images)

    def __run_process__(self, fonction, para1, para2):
        for i in range(self.nbr_process - 1, -1, -1):
            process = multiprocessing.Process(target=fonction, args=(
                para1, para2, self.images[self.X_range_process[i][0]: self.X_range_process[i][1]]))
            process.start()
            self.running_process.append(process)

        for process in self.running_process:
            process.join()

        self.running_process = []


def __process_rescale__(height, width, X):
    """
    :param X: sous partie de self.images à exécuter par le process
    """
    for img in X:
        img.rescale(height, width)


def __process_resize__(height, width, X):
    """
    :param X: sous partie de self.images à exécuter par le process
    """
    for img in X:
        img.resize(height, width)


def __process_crop__(height, width, X):
    """
    :param X: sous partie de self.images à exécuter par le process
    """
    for img in X:
        img.crop(height, width)


def __process_unsharpGaussianFilter__(sigma, factor, X):
    """
    :param X: sous partie de self.images à exécuter par le process
    """
    for img in X:
        img.unsharpGaussianFilter(sigma, factor)
