import sys
from manim import *
import random

sys.path.insert(1, "ressource/creature")

from creature import *
from creature_scene import *

IMG_PATH = "ressource/images"
SIMPLE_IMAGE_PATH = "ressource/images/fleur_simple";
PAS_SIMPLE_IMAGE_PATH = "ressource/images/fleur_pas_simple";
LOUPE_PATH = IMG_PATH + "/loupe.svg"
ORDI_PATH = IMG_PATH + "/ordinateur"

random.seed(1212)#on utilise des mélanges mais c'est cool d'avoir la même vidéo entre 2 exécution

class Scene4(Scene):
    def construct(self):
        scale = 2
        ordinateur = Square().scale(scale)
        #ordinateur=ImageMobject(ORDI_PATH).scale(1.4).shift(LEFT+1*DOWN)
        #loupe = SVGMobject(LOUPE_PATH).scale(0.25)
        #loupe[0].set_color(WHITE)

        titre = Tex("Apprentissage")
        titre.shift(3*UP)
        self.add(titre)

        flowers = [] # liste de (ImageMobject, nom fleur)
        for file in os.listdir(SIMPLE_IMAGE_PATH):
            file_dir = os.path.join(SIMPLE_IMAGE_PATH, file) # chemin de l'image
            name = file.split("_")[0]
            obj = ImageMobject(file_dir)
            txt = Tex(name)

            flowers.append([
                obj,
                name,
                txt]
            )
        random.shuffle(flowers)

        #loupe.next_to(ordinateur, ORIGIN)
        self.add(ordinateur)

        for i in range(len(flowers)):
            image_obj = flowers[i][0]
            image_label = flowers[i][1]
            text_obj = flowers[i][2]

            image_obj.move_to(5*LEFT)
            text_obj.next_to(image_obj,DOWN)
            self.play(FadeIn(image_obj), FadeIn(text_obj))
            self.play(ApplyMethod(image_obj.move_to, ORIGIN), ApplyMethod(text_obj.next_to, ordinateur, DOWN))

            scan = Line(scale*LEFT+scale*UP,scale*RIGHT+scale*UP, color=GREEN)

            self.play(ShowCreation(scan))

            for i in range(2):
                if i%2:
                    sens = scale*UP
                else:
                    sens = scale*DOWN

                self.play(ApplyMethod(scan.shift, 2*sens))

            self.play(
                FadeOut(scan),
                FadeOut(image_obj),
                FadeOut(text_obj)
            )



        self.wait(5)
