from glob import glob

from skimage.filters import unsharp_mask
from skimage.io import imread, imsave

"""
Toutes ces fonctions peuvent prendre comme pathToImages un répertoire qui sera de manère récursive visité
pour traiter toutes les images au format choisis qu'il contient.
"""


def unsharpGaussianFilter(pathToImages, sigma=10, factor=2, format='png'):
    """
    https://scikit-image.org/docs/dev/auto_examples/filters/plot_unsharp_mask.html
    enhanced image = original + factor * (original - blurred)
    :param pathToImages: chemin jusqu'au repertoire contenant les images
    :param sigma: écart type pour la fonction de Gauss. Plus il est grand moins il y aura de flou.
    :param factor: facteur d'accentuation
    :param format: format des images, png ou jpg
    :return:
    """
    for imgPath in glob(pathToImages + "**/*." + format, recursive=True):
        image = imread(imgPath)
        unsharp = unsharp_mask(image, sigma, factor, multichannel=True)
        imsave(imgPath, unsharp)
