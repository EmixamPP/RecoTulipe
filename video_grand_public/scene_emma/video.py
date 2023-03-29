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

MY_COLOR = LIGHT_GRAY

TEXT_COLOR = WHITE


class GraphManualPosition(Scene):
    """
    def play(self,*args, **kwargs):
        if "run_time" not in kwargs:
            kwargs["run_time"] = 1

        kwargs["run_time"] /= 2

        super().play(*args, **kwargs)
    """


    def construct(self):
        self.camera.background_color = WHITE
        self.net = Network([6,4,4], (0,0), 5,1.3, edge_config={"color":MY_COLOR}, vertex_config={"color":BLACK,"radius":.4, "fill_opacity":1})
        self.cells = [self.net.get_neurones_on_layer(i) for i in range(3)]


        self.add(self.net)

        #self.backPropagation()
        self.forwardPass()

    def write_cell_name(self, to_write, cell_num, *layers):
        """
        param to_write: liste d'entier à ecrire dans neurones
        pram layers: liste des couches à afficher noms des neurones
        """
        for j in range(len(layers)):
            layer = layers[j]
            to_write_in_cell = []
            if (cell_num == -1):
                for i in range(len(self.cells[layer])):
                    to_write_in_cell.append((self.cells[layer][i],str(to_write[j][i])))
            else:
                to_write_in_cell.append((self.cells[layer][::-1][cell_num],str(to_write[j][::-1][cell_num])))

            t = self.net.write_in_vertices(to_write_in_cell, color=TEXT_COLOR)
            t = list(map(Write, t))
            self.play(*t)

    def write_cell_name_bp(self, to_write, *layers):
        """
        param to_write: liste d'entier à ecrire dans neurones
        pram layers: liste des couches à afficher noms des neurones
        """
        to_write_in_cell = []
        for j in range(len(layers)):
            layer = layers[j]
            for i in range(len(self.cells[layer])):
                to_write_in_cell.append((self.cells[layer][i],str(to_write[j][i])))

        t = self.net.write_in_vertices(to_write_in_cell, color=TEXT_COLOR)
        t = list(map(Write, t))
        self.play(*t)

    def lines_to_animate(self, layers):
        res = []
        for i in self.cells[layers[1]]:
            lines = []
            for j in self.cells[layers[0]]:
                lines.append((j,i))
            res.append(lines)
        return res[::-1]

    def forwardPass(self):
        cell_values = [[0,0,1,1],[0,0,0,0]]
        speed = [6,1]
        is_first = True

        self.write_cell_name([[1,0,0,1,0,1]], -1, 0)
        self.wait(12)

        for i in range(2):
            #anime lignes
            line_layer12 = self.lines_to_animate((i,i+1))
            all_lines = []
            cell_num = 0
            for cell in line_layer12:
                lines = self.net.create_edge_copy(cell, color=RED)
                all_lines += lines
                animations = map(ShowCreation, lines)
                self.play(*animations,run_time = speed[not is_first])
                if is_first: self.wait(4)
                is_first = False
                self.write_cell_name([cell_values[i]], cell_num, i+1) #ecrit valeurs dans neurones
                cell_num += 1

            self.net.clean();

            self.wait(6)

            for i in all_lines:
                i.set_color(MY_COLOR)

            self.wait(1)

    def animate_solution(self):
        signes = ["$\\neq$","$=$","$=$","$=$"]
        cell_value = [1,0,0,0]
        anim_signes = []
        anim_cell = []
        for i in range(4):
            s = Tex(signes[i], color=BLACK)
            s.next_to(self.net[self.cells[2][i]],RIGHT)
            anim_signes.append(FadeIn(s))

            vertice = self.net.get_copy_vertice()
            vertice.next_to(s,RIGHT)
            anim_cell.append(FadeIn(vertice))
            val = Tex(str(cell_value[i]), color=TEXT_COLOR)
            val.next_to(vertice,ORIGIN)
            anim_cell.append(FadeIn(val))

        self.play(*anim_cell)
        self.wait()
        self.play(*anim_signes)
        self.wait()

    def get_lines_to_draw_bp(self, *layers):
        lines = []
        if layers == (2,1):
            for i in self.cells[layers[1]]:
                lines.append((self.cells[layers[0]][0], i))
            self.wait(2)
        else:
            signes = ["$0\\neq1$","$0\\neq1$","$1=1$","$1=1$"]
            anim_signes = []
            for i in range(4):
                s = Tex(signes[i], color=BLACK).scale(.5)
                s.next_to(self.net[self.cells[1][i]],0.5*UP)
                anim_signes.append(FadeIn(s))

            self.play(*anim_signes)
            self.wait(16)

            lines = [(self.cells[layers[0]][0], self.cells[layers[1]][0]),
                    (self.cells[layers[0]][0], self.cells[layers[1]][3]),
                    (self.cells[layers[0]][0], self.cells[layers[1]][5]),
                    (self.cells[layers[0]][1], self.cells[layers[1]][0]),
                    (self.cells[layers[0]][1], self.cells[layers[1]][3]),
                    (self.cells[layers[0]][1], self.cells[layers[1]][5]),
                    ]

        lines_copy = self.net.create_edge_copy(lines, True, color=RED)
        animations = map(ShowCreation, lines_copy)
        self.play(*animations)


    def animate_correction(self):
        for i in range(2,0,-1):
            self.get_lines_to_draw_bp(i,i-1)

    def backPropagation(self):
        self.write_cell_name_bp([[1,0,0,1,0,1],[0,0,1,1],[0,0,0,0]], 0,1,2)
        self.wait()
        self.animate_solution()
        self.wait(3)
        self.animate_correction()
        self.wait(8)
