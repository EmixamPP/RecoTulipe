import imageio.core.util
import numpy as np
import skimage.color
import skimage.filters
import skimage.io
import skimage.transform


def ignore_warnings(*args, **kwargs):
    pass


imageio.core.util._precision_warn = ignore_warnings


class Image:
    def __init__(self, image, label):
        """
        :param image: peurendre soit le chemin vers une image, soit la représentation matricielle d'une image
        :param label: label à associer à l'image
        """
        if type(image) is str:
            self.image = skimage.io.imread(image)
        else:
            self.image = np.array(image)

        self.label = label

    def rescale(self, height, width):
        """
        Redimentionne l'image en gardant le radio. Ex: sur une image en 2000x1000 vers 224x224
        l'image finale sera de 448x224. Autrement dit le rescale ce fait en fonction du plus petit.
        :param height: hauteur voulue
        :param width: largeur voulue
        :return:
        """
        oldH = self.image.shape[0]
        oldW = self.image.shape[1]
        factor = oldW / width if oldW < oldH else oldH / height

        self.image = skimage.transform.rescale(self.image, 1 / factor, multichannel=(len(self.image.shape) == 3))
        self.image *= 255  # on remet les valeurs entre 0 et 255

    def resize(self, height, width):
        """
        Redimentionne l'image en ignorant le radio
        :param height: hauteur voulue
        :param width: largeur voulue
        :return:
        """
        self.image = skimage.transform.resize(self.image, (height, width, self.image.shape[2]))
        self.image *= 255  # on remet les valeurs entre 0 et 255

    def crop(self, height, width):
        """
        Coupe l'image à partir du centre de celle-ci. Si l'image est plus petite elle sera resize.
        :param height: hauteur voulue
        :param width: largeur voulue
        :return:
        """
        oldH = self.image.shape[0]
        oldW = self.image.shape[1]
        if oldH < height or oldW < width:
            self.resize(height, width)
        else:
            newW = oldW // 2 - (width // 2)
            newY = oldH // 2 - (height // 2)
            self.image = self.image[newY:newY + height, newW:newW + width, :]

    def save(self, pathToSave):
        """
        Enregistre l'image à un emplacement donné
        :param pathToSave: emplacement à enregistrer l'image
        :return:
        """
        skimage.io.imsave(pathToSave, self.image)

    def getLabel(self):
        """
        :return: le label associé à l'image
        """
        return self.label

    def getSize(self):
        """
        :return: un tuple (largeur, hauteur) de l'image en pixels
        """
        return self.image.shape[0:2]

    def unsharpGaussianFilter(self, sigma=5, factor=2):
        """
        Supprime le bruit/flou des images
        https://scikit-image.org/docs/dev/auto_examples/filters/plot_unsharp_mask.html
        L'idée principale est la suivante : les détails nets sont identifiés comme la différence entre l'image originale
        et sa version floue. Ces détails sont ajoutés à l'image originale après une étape de mise à l'échelle :
        enhanced image = original + factor * (original - blurred)
        :param sigma: écart type pour la fonction de Gauss. Plus il est grand moins il y aura de flou.
        :param factor: facteur d'accentuation
        :return:
        """
        self.image = skimage.filters.unsharp_mask(self.image, sigma, factor, multichannel=(len(self.image.shape) == 3))
        self.image *= 255  # on remet les valeurs entre 0 et 255

    def repr(self, gray=False):
        """
        :param gray: si vrai l'image sera donné en nuance de gris (2D) dans le cas où elle est en couleur
        :return: la représentation matricielle de l'image (np.ndarray)
        """
        if gray and self.image.shape == 3:
            colordim = self.image.shape[2]
            if colordim == 4:  # rgba
                return skimage.color.rgb2gray(skimage.color.rgba2rgb(self.image))
            elif colordim == 3:  # rgb
                return skimage.color.rgb2gray(self.image)

        return self.image
