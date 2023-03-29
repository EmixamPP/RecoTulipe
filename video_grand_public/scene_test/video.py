import sys
from manim import *
import random

sys.path.insert(1, "ressource/creature")
sys.path.insert(1, "ressource/neuralNet")

from creature import *
from creature_scene import *
from network import *

SIMPLE_IMAGE_PATH = "ressource/images/fleur_simple";

random.seed(12)#on utilise des mélanges mais c'est cool d'avoir la même vidéo entre 2 exécution

"""class Main(CreatureScene):
    def construct(self):
        super().construc(creatures_start_on_screen=False)"""

class GraphManualPosition(Scene):
    def construct(self):
        net = Network([3,4,2], (0,0), 2,1)

        self.add(net)


        self.wait(1)

        #net.shift(2*RIGHT + UP)
        self.play(ApplyMethod(net.shift, 2*RIGHT + UP))

        t = net.write_in_vertices([
        (0,"1"),
        (5,"12")
        ])

        t = list(map(Write, t))

        self.play(*t)

        #ligne = net.edges[(0,3)]

        #self.play(FadeToColor(ligne, RED))
        #self.remove(ligne)
        #ligne.set_color(RED)
        #self.play(ShowCreation(ligne))

        #self.play(*t)

        ligne = net.create_edge_copy((0,3), color=RED)

        self.play(ShowCreation(ligne))

        self.wait(2)

        net.shift(3*LEFT)

        self.wait(2)

        ligne.shift(3*RIGHT)
        self.wait()
