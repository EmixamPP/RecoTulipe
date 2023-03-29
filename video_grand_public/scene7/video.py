import sys
from manim import *
import random

sys.path.insert(1, "ressource")
sys.path.insert(1, "ressource/neuralNet")

from image_loader import *
from generate_title import *
from network import *

IMG_PATH = "ressource/images"
TRAINING_FLOWERS= "ressource/images/fleur_apprentissage";
TESTING_FLOWERS= "ressource/images/fleur_test";
FLOWERS_NAMES = ["tournesol", "tulipe", "paquerette"]

random.seed(121212)#on utilise des mélanges mais c'est cool d'avoir la même vidéo entre 2 exécution

DIALOGUE_SPEED = 0.5

class Scene7(Scene):
    def construct(self):
        layers = [7,4,4,3]
        self.net = Network(layers,
            (0,-.5),
            hDist = 3,
            vDist = 1,
            vertex_config = {"radius": .3, "fill_opacity":1, "color":BLACK, "stroke_width": 2, "stroke_color":WHITE},
            edge_config = {"color":BLACK}
            )

        titre = generate_title(self, "Aller plus loin")

        self.set_vertex_color(self.net.get_neurones_on_layer(0))
        self.play(FadeIn(self.net))
        self.wait(2)

        run_time = 2
        first = True
        for layer_index in range(1,len(layers)):
            edges_list = []
            first = True
            run_time = 2
            for neurone_index in self.net.get_neurones_on_layer(layer_index)[::-1]:
                for previous_neurone_index in self.net.get_neurones_on_layer(layer_index-1):
                    edges_list.append((previous_neurone_index, neurone_index))

                self.animate_edges(edges_list, run_time=run_time)
                self.set_vertex_color([neurone_index])
                if first:
                    run_time /= 4
                    first = False


        self.wait()
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])



    def animate_edges(self, edges, run_time=1):

        lines = self.net.create_edge_copy(edges, color=WHITE)
        self.net.clean()
        lines = [ShowCreation(l) for l in lines]
        edges[:] = []
        self.play(*lines, run_time=run_time)

    def set_vertex_color(self, vertex_list, run_time=1):
        animations = []
        for vertex_index in vertex_list:
            vertex = self.net[vertex_index]
            #animations.append(ApplyMethod(vertex.set_fill, self.get_random_gray()))
            vertex.set_fill(self.get_random_gray())

        #self.play(*animations, run_time=run_time)

    def get_random_gray(self):
        nuance = random.randint(0,255)
        res = "#{0}{0}{0}".format(format(nuance, "02x"))
        return res
