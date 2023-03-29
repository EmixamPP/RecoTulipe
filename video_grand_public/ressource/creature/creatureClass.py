from manim import *
from drawings import *


class CreatureClass(VGroup):
    DEFAULT_CONFIG = {
        "width": 3,
        "height": 2
    }

    def __init__(self, **kwargs):
        kwargs=extract_kwargs(self, self.DEFAULT_CONFIG, **kwargs)
        VGroup.__init__(self, **kwargs)
        for i in range(self.width):
            for j in range(self.height):
                pi = Creature().scale(0.3)
                pi.move_to(i * DOWN + j * RIGHT)
                self.add(pi)
