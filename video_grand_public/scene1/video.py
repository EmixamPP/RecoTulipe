import sys
from manim import *
import random

sys.path.insert(1, "ressource/creature")

from creature import *
from creature_scene import *

SIMPLE_IMAGE_PATH = "ressource/images/fleur_simple";
PAS_SIMPLE_IMAGE_PATH = "ressource/images/fleur_pas_simple";

random.seed(1212)#on utilise des mélanges mais c'est cool d'avoir la même vidéo entre 2 exécution

class Scene1(CreatureScene):
    def construct(self):
        super().construct()

        #oct=Octavius().to_edge(DOWN+LEFT).scale(0.8)

        flowers = [] # liste de (ImageMobject, nom fleur)
        for file in os.listdir(SIMPLE_IMAGE_PATH):
            file_dir = os.path.join(SIMPLE_IMAGE_PATH, file) # chemin de l'image
            flowers.append((ImageMobject(file_dir), file.split("_")[0]))
        random.shuffle(flowers)

        previous=None
        animation_time = 1.0

        pos = [
            (-1,2),
            (4,2),
            (-1,-2),
            (4,-2)
        ]

        self.wait(3)
        for i in range(len(flowers)):
            image_obj = flowers[i][0]
            image_label = flowers[i][1]

            image_obj.move_to(pos[i][0]*RIGHT+pos[i][1]*UP)

            self.play(FadeIn(image_obj), ApplyMethod(self.creature.look_at,image_obj), run_time=animation_time)
            self.say("C'est {}".format(image_label), bubble_kwargs = {"height" : 3, "width" : 4},          target_mode="speaking", run_time=animation_time)

            self.wait(animation_time)
            self.remove(self.creature.bubble, self.creature.bubble.content)

            if i== 5:
                animation_time = .2

        self.wait(1)

        flowers = [] # liste de ImageMobject
        for file in os.listdir(PAS_SIMPLE_IMAGE_PATH):
            file_dir = os.path.join(PAS_SIMPLE_IMAGE_PATH, file) # chemin de l'image
            flowers.append(ImageMobject(file_dir))
        random.shuffle(flowers)

        pos=[]
        x_possible = [x for x in range(-1,5,1)]#liste des positions possibles
        y_possible = [y for y in range(-3,4,1)]
        for x in x_possible:
            for y in y_possible:
                pos.append((x,y,0))
        random.shuffle(pos)
        print("Len: ",len(pos))

        run_time = 0.7
        for image_obj in flowers:

            image_obj.move_to(pos.pop())

            animation = [FadeIn(image_obj), ApplyMethod(self.creature.look_at,image_obj)]
            self.play(*animation, run_time=run_time)

        self.wait()

        self.think("C'est trop dur...", bubble_kwargs = {"height" : 3, "width" : 4}, target_mode="sad")
        self.play(ApplyMethod(self.creature.look_at,3*DOWN))
        self.wait(3)
        self.remove(self.creature.bubble, self.creature.bubble.content)

        self.say("Est-ce qu'un ordinateur\\\\pourrait faire le travail\\\\ à ma place?", bubble_kwargs = {"height" : 4, "width" : 6}, target_mode="speaking")

        self.wait(8)
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
