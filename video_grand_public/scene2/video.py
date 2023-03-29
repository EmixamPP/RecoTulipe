import sys
from manim import *
import random

sys.path.insert(1, "ressource/creature")
sys.path.insert(1, "ressource")

from creature import *
from creature_scene import *
from generate_title import *

IMG_PATH = "ressource/images"
SIMPLE_IMAGE_PATH = "ressource/images/fleur_simple";
PAS_SIMPLE_IMAGE_PATH = "ressource/images/fleur_pas_simple";
COMPUTER_PATH = "ressource/images/moniteur.svg"
LOUPE_PATH = IMG_PATH + "/loupe.svg"
ORDI_PATH = IMG_PATH + "/ordinateur"

random.seed(1212)#on utilise des mélanges mais c'est cool d'avoir la même vidéo entre 2 exécution

class Scene2(Scene):
    def construct(self):
        titre = generate_title(self, "objectif",wait_time=0.5)

        SCANNER_ANIMATION_TIME = 0.5


        scale = 2
        scan = Line(scale*LEFT+scale*UP,scale*RIGHT+scale*UP, color=GREEN).shift(0.6*DOWN)
        shift_scale = 1.25

        #ordinateur = ImageMobject(COMPUTER_PATH).scale(3.3).shift(0.35*DOWN)
        ordinateur = SVGMobject(COMPUTER_PATH).scale(2).shift(0.35*DOWN)
        ordinateur[0].set_color(GRAY)
        #ordinateur = Square().scale(2)
        #ordinateur=ImageMobject(ORDI_PATH).scale(1.4).shift(LEFT+1*DOWN)
        #loupe = SVGMobject(LOUPE_PATH).scale(0.25)
        #loupe[0].set_color(WHITE)

        #titre = Tex("Objectif")
        #titre.shift(3*UP)
        #self.add(titre)

        scan.set_z_index(-1)
        ordinateur.set_z_index(100)


        flowers = [] # liste de (ImageMobject, nom fleur)
        for file in os.listdir(SIMPLE_IMAGE_PATH):
            file_dir = os.path.join(SIMPLE_IMAGE_PATH, file) # chemin de l'image
            flowers.append([ImageMobject(file_dir), file.split("_")[0]])
        random.shuffle(flowers)

        #loupe.next_to(ordinateur, ORIGIN)
        #self.add(ordinateur)
        #self.play(FadeIn(ordinateur), run_time=0.5)

        WAIT = 0.75

        previous = -1
        anim = []
        for i in range(len(flowers)):
            text_obj = Tex(flowers[i][1])
            flowers[i].append(text_obj)
            if previous == -1:
                text_obj.move_to(5*RIGHT+1.5*UP)
            else:
                text_obj.next_to(previous, 3*DOWN)
            previous = text_obj
            anim.append(FadeIn(text_obj))

        anim.append(FadeIn(ordinateur))
        self.play(*anim)
        self.add(scan)

        for i in range(len(flowers)):
            image_obj = flowers[i][0]
            image_label = flowers[i][1]
            text_obj = flowers[i][2]

            #la fleur se déplace vers le centre
            image_obj.set_z_index(-2)
            image_obj.move_to(5*LEFT)
            self.play(FadeIn(image_obj),run_time=WAIT)
            self.play(ApplyMethod(image_obj.move_to, ORIGIN), run_time=WAIT)

            #barre qui scan la  fleur
            #self.play(ShowCreation(scan))
            for i in range(2):
                if i%2:
                    sens = shift_scale*UP
                else:
                    sens = shift_scale*DOWN
                self.play(ApplyMethod(scan.shift, 2*sens), run_time=SCANNER_ANIMATION_TIME)

            #self.wait()
            self.play(ApplyMethod(image_obj.scale,.2), WAIT = 0.75)
            self.play(
                ApplyMethod(image_obj.next_to, text_obj, LEFT),
                WAIT = 0.75
            )
        #self.add(loupe)

        self.wait(1)

        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
