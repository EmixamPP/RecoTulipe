from manim import *
from drawings import *
from creatureClass import *


class Blink(ApplyMethod):
    DEFAULT_CONFIG = {
        "rate_func": squish_rate_func(there_and_back)
    }

    def __init__(self, creature, **kwargs):
        kwargs=extract_kwargs(self, self.DEFAULT_CONFIG, **kwargs)
        ApplyMethod.__init__(self, creature.blink, **kwargs)


class CreatureBubbleIntroduction(AnimationGroup):
    DEFAULT_ROOT_CONFIG = {
        "target_mode": "speaking",
        "bubble_class": SpeechBubble,
        "change_mode_kwargs": {},
        "bubble_creation_class": DrawBorderThenFill,
        "bubble_creation_kwargs": {},
        "bubble_kwargs": {},
        "content_introduction_class": Write,
        "content_introduction_kwargs": {},
        "look_at_arg": None,
    }

    DEFAULT_CONFIG = {}

    def __init__(self, creature, *content, **kwargs):
        #print(kwargs)
        kwargs=extract_kwargs(self, self.DEFAULT_CONFIG, **kwargs)
        kwargs=extract_kwargs(self, self.DEFAULT_ROOT_CONFIG, **kwargs)
        #print(kwargs)
        #input(">>")
        bubble = creature.get_bubble(
            *content,
            bubble_class=self.bubble_class,
            **self.bubble_kwargs
        )
        Group(bubble, bubble.content).shift_onto_screen()

        if "direction" in self.bubble_kwargs and self.bubble_kwargs["direction"][0] > 0:
            Group(bubble, bubble.content).shift(-self.bubble_kwargs["direction"])
        creature.generate_target()
        creature.target.change_mode(self.target_mode)
        if self.look_at_arg is not None:
            creature.target.look_at(self.look_at_arg)

        change_mode = MoveToTarget(creature, **self.change_mode_kwargs)
        bubble_creation = self.bubble_creation_class(
            bubble, **self.bubble_creation_kwargs
        )
        content_introduction = self.content_introduction_class(
            bubble.content, **self.content_introduction_kwargs
        )
        AnimationGroup.__init__(
            self, change_mode, bubble_creation, content_introduction,
            **kwargs
        )


class CreatureSays(CreatureBubbleIntroduction):
    DEFAULT_CONFIG = {
        "target_mode": "speaking",
        "bubble_class": SpeechBubble,
    }


class RemoveCreatureBubble(AnimationGroup):
    DEFAULT_CONFIG = {
        "target_mode": "plain",
        "look_at_arg": None,
        "remover": True,
    }

    def __init__(self, creature, **kwargs):
        assert hasattr(creature, "bubble")
        kwargs=extract_kwargs(self, self.DEFAULT_CONFIG, **kwargs)

        self.creature = creature
        creature.generate_target()
        creature.target.change_mode(self.target_mode)
        if self.look_at_arg is not None:
            creature.target.look_at(self.look_at_arg)

        AnimationGroup.__init__(
            self,
            MoveToTarget(creature),
            FadeOut(creature.bubble),
            FadeOut(creature.bubble.content),
        )

    def clean_up_from_scene(self, scene=None):
        AnimationGroup.clean_up_from_scene(self, scene)
        self.creature.bubble = None
        if scene is not None:
            scene.add(self.creature)


class FlashThroughClass(Animation):
    DEFAULT_CONFIG = {
        "highlight_color": GREEN,
    }

    def __init__(self, mobject, mode="linear", **kwargs):
        if not isinstance(mobject, CreatureClass):
            raise Exception("FlashThroughClass mobject must be a CreatureClass")
        digest_config(self, kwargs)
        self.indices = list(range(mobject.height * mobject.width))
        if mode == "random":
            np.random.shuffle(self.indices)
        Animation.__init__(self, mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        index = int(np.floor(alpha * self.mobject.height * self.mobject.width))
        for pi in self.mobject:
            pi.set_color(BLUE_E)
        if index < self.mobject.height * self.mobject.width:
            self.mobject[self.indices[index]].set_color(self.highlight_color)
