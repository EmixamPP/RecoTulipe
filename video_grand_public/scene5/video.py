import sys
from manim import *
import random

sys.path.insert(1, "ressource/creature")
sys.path.insert(1, "ressource")

from creature import *
from creature_scene import *
from image_loader import *
from generate_title import *
from math import pi, sin, cos

IMG_PATH = "ressource/images"
TRAINING_FLOWERS= "ressource/images/fleur_apprentissage";
TESTING_FLOWERS= "ressource/images/fleur_test";
FLOWERS_NAMES = ["tournesol", "tulipe", "paquerette"]
COMPUTER_PATH = "ressource/images/moniteur.svg"


random.seed(121212)#on utilise des mélanges mais c'est cool d'avoir la même vidéo entre 2 exécution

DIALOGUE_SPEED = 0.5

class Scene5(Scene):
    def construct(self):
        super().construct()

        learn_flowers = load_flower(TRAINING_FLOWERS, FLOWERS_NAMES, 1)
        random.shuffle(learn_flowers)

        test_flowers = load_flower(TESTING_FLOWERS, FLOWERS_NAMES, 1)

        titre = generate_title(self, "Comment utiliser tous ces pixels?")

        computer = SVGMobject(COMPUTER_PATH).scale(2.5)
        computer[0].set_color(GRAY)
        #self.add(computer)
        group = []
        names = []
        for flower in test_flowers:
            imgObj = flower[0].scale(3)
            name = flower[1]

            imgObj.move_to(ORIGIN)
            self.play(FadeIn(imgObj))

            #self.wait()

            self.play(ApplyMethod(imgObj.shift, 3*LEFT))
            tournesol = None
            names.append(name)
            if name == "paquerette":
                forme = self.getPaqueretteForme()
            elif name == "tournesol":
                forme = self.getTournesol()
            elif name == "tulipe":
                forme = self.getTulipe()

            forme.shift(3*RIGHT)
            self.play(ShowCreation(forme))
            self.wait()

            new = Group(imgObj, forme)
            self.play(FadeOut(new))
            new.scale(0.4)
            if len(group):
                last = group[-1]
                new.next_to(last,DOWN)
            else:
                new.move_to(2*UP+ORIGIN)


            group.append(new)

        self.play(*[FadeIn(el) for el in group])

        self.wait(4)

        for i in range(len(group)):
            forme = group[i][1]
            if names[i] == "paquerette":
                forme[-2].set_color(YELLOW)
                for obj in forme[:-2]:
                    obj.set_fill(color=WHITE, opacity=1)
            elif names[i] == "tournesol":
                for obj in forme[:-2]:
                    obj.set_fill(color=YELLOW, opacity=1)

            elif names[i] == "tulipe":
                forme[0].set_color(GREEN)
                forme[1].set_fill(color=GREEN, opacity=1)
                forme[1].set_color(GREEN)
                forme[2].set_color(RED)
                forme[3].set_color(RED)

        self.wait(3)

        self.play(*[FadeOut(mobj) for mobj in self.mobjects])

    def getPaqueretteForme(self):
        return self.getSimpleFlower(1,15,1.5)

    def getTournesol(self):
        return self.getSimpleFlower(1.5,12,1)

    def getSimpleFlower(self, radius, numberPetal, petalHeight):
        res = VGroup()

        center = Circle(radius=radius, color=WHITE, stroke=2)

        orientations = [i*pi/(numberPetal/2) for i in range(numberPetal)]

        width = 2*pi*radius / numberPetal  # largeur d'un pétale à la base
        for orientation in orientations:#ajoute tous les pétales

            petal = Ellipse(width=width, height=1.5, color=WHITE).rotate(-orientation)

            xShift = sin(orientation) * radius * petalHeight * 1.15
            yShift = cos(orientation) * radius * petalHeight * 1.15
            petal.shift([xShift,yShift,0])

            res.add(petal)

        mask = Circle(radius=radius, color=BLACK, fill_opacity=1)
        res.add(mask)
        res.add(center)

        return res

    def getTulipe(self):
        res = VGroup()

        tige = Line(DOWN,UP,stroke_width=5, color=WHITE)
        res.add(tige)

        feuille = Ellipse(width=0.5, height=1.5,color=WHITE).rotate(pi/4).shift(UP/4+LEFT*0.55)
        res.add(feuille)

        fleur1 = ArcBetweenPoints(ORIGIN, LEFT/3+UP, angle=-pi/2)
        fleur2 = ArcBetweenPoints(ORIGIN, RIGHT/3+UP)

        fleur1.shift(UP)
        fleur2.shift(UP)

        res.add(fleur1,fleur2)
        return res
