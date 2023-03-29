from manim import *

class Test(Scene):
    def construct(self):
        l = Line(2*LEFT,2*RIGHT)
        self.play(ShowCreation(l))
        self.wait(1)
