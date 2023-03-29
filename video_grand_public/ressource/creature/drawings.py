from manim import *
import os
#from manim.utils.config_ops import digest_config

FILE_DIR = "./ressource/creature/"

def extract_kwargs(object, default_conf, **kwargs):
    """
    construit les kwargs en fonction de ceux donnés et de la config par défaut
    """
    kwargs = {**default_conf, **kwargs}
    object.__dict__.update(kwargs)
    return kwargs

class Bubble(SVGMobject):
    DEFAULT_ROOT_CONFIG = {
        "direction": LEFT,
        "center_point": ORIGIN,
        "content_scale_factor": 0.75,
        "height": 5,
        "width": 8,
        "bubble_center_adjustment_factor": 1. / 8,
        "file_name": None,
        "fill_color": BLACK,
        "fill_opacity": 0.8,
        "stroke_color": WHITE,
        "stroke_width": 3,
    }
    DEFAULT_CONFIG = {}
    def __init__(self, **kwargs):
        kwargs = extract_kwargs(self, self.DEFAULT_CONFIG, **kwargs)
        kwargs = extract_kwargs(self, self.DEFAULT_ROOT_CONFIG, **kwargs)

        if self.file_name is None:
            raise Exception("Must invoke Bubble subclass")
        try:
            SVGMobject.__init__(self, **kwargs)
        except IOError as err:
            self.file_name = os.path.join(FILE_DIR, self.file_name)
            kwargs["file_name"] = self.file_name
            SVGMobject.__init__(self, **kwargs)
        self.center()
        self.stretch_to_fit_height(self.height)
        self.stretch_to_fit_width(self.width)
        if self.direction[0] > 0:
            self.flip()
        self.direction_was_specified = ("direction" in kwargs)
        self.content = Mobject()

    def get_tip(self):
        # TODO, find a better way
        return self.get_corner(DOWN + self.direction) - 0.6 * self.direction

    def get_bubble_center(self):
        factor = self.bubble_center_adjustment_factor
        return self.get_center() + factor * self.get_height() * UP

    def move_tip_to(self, point):
        mover = VGroup(self)
        if self.content is not None:
            mover.add(self.content)
        mover.shift(point - self.get_tip())
        return self

    def flip(self, axis=UP):
        Mobject.flip(self, axis=axis)
        if abs(axis[1]) > 0:
            self.direction = -np.array(self.direction)
        return self

    def pin_to(self, mobject):
        mob_center = mobject.get_center() + self.center_point
        want_to_flip = np.sign(mob_center[0]) != np.sign(self.direction[0])
        can_flip = not self.direction_was_specified
        if want_to_flip and can_flip:
            self.flip()
        boundary_point = mobject.get_critical_point(UP - self.direction)
        vector_from_center = 1.0 * (boundary_point - mob_center)
        self.move_tip_to(mob_center + vector_from_center)
        return self

    def position_mobject_inside(self, mobject):
        scaled_width = self.content_scale_factor * self.get_width()
        if mobject.get_width() > scaled_width:
            mobject.set_width(scaled_width)
        mobject.shift(
            self.get_bubble_center() - mobject.get_center()
        )
        return mobject

    def add_content(self, mobject):
        self.position_mobject_inside(mobject)
        self.content = mobject
        return self.content

    def write(self, *text):
        self.add_content(Tex(*text))
        return self

    def resize_to_content(self):
        target_width = self.content.get_width()
        target_width += max(MED_LARGE_BUFF, 2)
        target_height = self.content.get_height()
        target_height += 2.5 * LARGE_BUFF
        tip_point = self.get_tip()
        self.stretch_to_fit_width(target_width)
        self.stretch_to_fit_height(target_height)
        self.move_tip_to(tip_point)
        #self.position_mobject_inside(self.contentblink)

    def clear(self):
        self.add_content(VMobject())
        return self


class SpeechBubble(Bubble):
    DEFAULT_CONFIG={
        "file_name":"Bubbles_speech",
        "height": 4
    }

class DoubleSpeechBubble(Bubble):
    DEFAULT_CONFIG={
        "file_name":"Bubbles_double_speech",
        "height": 4
    }

class ThoughtBubble(Bubble):
    DEFAULT_CONFIG ={
        "file_name":"Bubbles_thought"
    }
    def __init__(self, **kwargs):
        Bubble.__init__(self, **kwargs)
        self.submobjects.sort(
            key=lambda m: m.get_bottom()[1]
        )

    def make_green_screen(self):
        self.submobjects[-1].set_fill(GREEN_SCREEN, opacity=1)
        return self
