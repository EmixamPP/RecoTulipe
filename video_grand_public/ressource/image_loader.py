from manim import *
import os
import random

def load_flower(path, folder, n=None):
    """
    :param path: Che min d'un dossier
    :param folder: liste de nom de sous dossier de path
    :param n: nombre d'image que l'on veut par dossier (par défaut toutes les images du dossier)

    :return: liste de tuple (ImageMobject, nom de l'image). Le nom de l'image est le nom du dossier dans lequel elle se trouve
    """
    flowers = [] # liste de (ImageMobject, nom fleur)
    for name in folder:
        p = os.path.join(path, name)
        limit = n or min(n, len(os.listdir(p)))
        for file in os.listdir(p)[:limit]:
            file_dir = os.path.join(p, file) # chemin de l'image
            flowers.append((ImageMobject(file_dir), name))
    return flowers
