from glob import glob

from PIL import Image

"""
Toutes ces fonctions peuvent prendre comme pathToImages un répertoire qui sera de manère récursive visité
pour traiter toutes les images au format choisis qu'il contient.
"""


def reduce(pathToImages, width, height, format='png'):
    """
    Redimentionne l'image en gardant le radio
    :param pathToImages: chemin jusqu'au repertoire contenant les images
    :param width: largeur voulue
    :param height: hauteur voulue
    :param format: format des images, png ou jpg
    :return:
    """
    for imgPath in glob(pathToImages + "**/*." + format, recursive=True):
        image = Image.open(imgPath)
        image = image.thumbnail((width, height))
        image.save(imgPath)


def resize(pathToImages, width, height, format='png'):
    """
    Redimentionne l'image en ignorant le radio
    :param pathToImages: chemin jusqu'au repertoire contenant les images
    :param width: largeur voulue
    :param height: hauteur voulue
    :param format: format des images, png ou jpg
    :return:
    """
    for imgPath in glob(pathToImages + "**/*." + format, recursive=True):
        image = Image.open(imgPath)
        image = image.resize((width, height))
        image.save(imgPath)


def crop(pathToImages, width, height, format='png'):
    """
    Coupe l'image à partir du centre de celle-ic
    :param pathToImages: chemin jusqu'au repertoire contenant les images
    :param width: largeur voulue
    :param height: hauteur voulue
    :param format: format des images, png ou jpg
    :return:
    """
    for imgPath in glob(pathToImages + "**/*." + format, recursive=True):
        image = Image.open(imgPath)
        oldW, oldH = image.size
        if oldH < height or oldW < width:
            print(imgPath, "ignorée car sa taille est plus petite que celle demandée")
        else:
            left = (oldW - width) / 2
            top = (oldH - height) / 2
            right = (oldW + width) / 2
            bot = (oldH + height) / 2
            image = image.crop((left, top, right, bot))
            image.save(imgPath)
